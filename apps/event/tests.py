from datetime import datetime
from io import BytesIO
from unittest.mock import Mock, patch
from zoneinfo import ZoneInfo

import requests
from django.core.files.images import ImageFile
from django.test import TestCase, override_settings
from PIL import Image as PILImage
from rest_framework.test import APIClient
from wagtail.images import get_image_model
from wagtail.models import Page

from apps.event.models import EventIndexPage, EventPage
from apps.home.models import HomePage

HELSINKI = ZoneInfo('Europe/Helsinki')
IMAGE_URL = 'https://example.com/events/tampere.png'

EVENT_PAYLOAD = {
    'slug': 'tampere-syksy-26',
    'title': 'Tapaaminen Tampereella 10/26',
    'intro': 'Avoin Glorantha-tapaaminen Tampereella.',
    'description': '<p>Aika ja paikka: <strong>la 17.10.2026</strong></p>',
    'location': 'Tampere',
    'location_exact': 'Tampere, Laiska Pelikaani',
    'start': '2026-10-17T10:00:00+03:00',
    'end': '2026-10-17T21:00:00+03:00',
    'go_live_at': '2026-08-31T15:47:26.742000+03:00',
    'image': IMAGE_URL,
}


def _png_bytes():
    buf = BytesIO()
    PILImage.new('RGB', (1, 1), color='red').save(buf, format='PNG')
    return buf.getvalue()


def _mock_image_response(*args, **kwargs):
    response = Mock()
    response.content = _png_bytes()
    response.headers = {'Content-Type': 'image/png'}
    response.raise_for_status = Mock()
    return response


def _url_items(page):
    return [
        {'title': block.value['title'], 'url': block.value['url']}
        for block in page.urls
        if block.block_type == 'urls'
    ]


@override_settings(EVENT_API_TOKEN='test-event-token')
class UpsertEventAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v2/upsert_event/'
        self.auth_headers = {'HTTP_X_API_KEY': 'test-event-token'}

        root = Page.get_first_root_node()
        home = HomePage(
            title='Home',
            slug='home',
            title_text='',
            title_subtext='',
        )
        root.add_child(instance=home)
        home.save_revision().publish()

        self.event_index = EventIndexPage(title='Tapahtumat', slug='tapahtumat', body=[])
        home.add_child(instance=self.event_index)
        self.event_index.save_revision().publish()

        self.image_patcher = patch('apps.event.api.requests.get', side_effect=_mock_image_response)
        self.mock_get = self.image_patcher.start()
        self.addCleanup(self.image_patcher.stop)

    def _post(self, data, **extra_headers):
        headers = {**self.auth_headers, **extra_headers}
        return self.client.post(self.url, data, format='json', **headers)

    def test_unauthorized_without_token(self):
        response = self.client.post(self.url, EVENT_PAYLOAD, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_event_page(self):
        response = self._post(EVENT_PAYLOAD)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'created')
        self.assertEqual(response.json()['slug'], 'tampere-syksy-26')

        page = EventPage.objects.get(slug='tampere-syksy-26')
        self.assertEqual(page.title, EVENT_PAYLOAD['title'])
        self.assertEqual(page.intro, EVENT_PAYLOAD['intro'])
        self.assertEqual(page.description, EVENT_PAYLOAD['description'])
        self.assertEqual(page.location, EVENT_PAYLOAD['location'])
        self.assertEqual(page.location_exact, EVENT_PAYLOAD['location_exact'])
        self.assertEqual(
            page.start,
            datetime(2026, 10, 17, 10, 0, tzinfo=HELSINKI),
        )
        self.assertIsNotNone(page.image)
        self.assertEqual(page.image.title, 'tampere-syksy-26')
        self.mock_get.assert_called_once()

    def test_update_event_page_by_slug(self):
        self._post(EVENT_PAYLOAD)
        updated = {**EVENT_PAYLOAD, 'intro': 'Päivitetty intro'}
        response = self._post(updated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'updated')

        page = EventPage.objects.get(slug='tampere-syksy-26')
        self.assertEqual(page.intro, 'Päivitetty intro')
        self.assertEqual(EventPage.objects.filter(slug='tampere-syksy-26').count(), 1)

    def test_unchanged_does_not_create_revision(self):
        self._post(EVENT_PAYLOAD)
        page = EventPage.objects.get(slug='tampere-syksy-26')
        revision_count = page.revisions.count()

        response = self._post(EVENT_PAYLOAD)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'unchanged')
        page.refresh_from_db()
        self.assertEqual(page.revisions.count(), revision_count)

    def test_fetches_image_per_event_slug(self):
        self._post(EVENT_PAYLOAD)
        other = {
            **EVENT_PAYLOAD,
            'slug': 'other-event',
            'title': 'Toinen tapahtuma',
        }
        response = self._post(other)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'created')

        image_model = get_image_model()
        self.assertEqual(image_model.objects.filter(title='tampere-syksy-26').count(), 1)
        self.assertEqual(image_model.objects.filter(title='other-event').count(), 1)
        self.assertEqual(self.mock_get.call_count, 2)

        first = EventPage.objects.get(slug='tampere-syksy-26')
        second = EventPage.objects.get(slug='other-event')
        self.assertNotEqual(first.image_id, second.image_id)

    def test_image_fetch_failure_returns_400(self):
        self.mock_get.side_effect = requests.RequestException('network down')
        response = self._post(EVENT_PAYLOAD)
        self.assertEqual(response.status_code, 400)
        self.assertIn('image', response.json())

    def test_uses_existing_image_by_title(self):
        image_model = get_image_model()
        existing = image_model(
            title='20251223_152727',
            file=ImageFile(BytesIO(_png_bytes()), name='20251223_152727.png'),
        )
        existing.save()

        payload = {**EVENT_PAYLOAD, 'image': '20251223_152727'}
        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'created')

        page = EventPage.objects.get(slug='tampere-syksy-26')
        self.assertEqual(page.image_id, existing.id)
        self.mock_get.assert_not_called()

    def test_missing_image_title_returns_400(self):
        payload = {**EVENT_PAYLOAD, 'image': '20251223_152727'}
        response = self._post(payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('image', response.json())
        self.mock_get.assert_not_called()

    def test_create_event_with_urls(self):
        payload = {
            **EVENT_PAYLOAD,
            'urls': [
                {'title': 'Facebook', 'url': 'https://facebook.com/events/123'},
                {'title': 'Ilmoittautuminen', 'url': 'https://example.com/signup'},
            ],
        }
        response = self._post(payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'created')

        page = EventPage.objects.get(slug='tampere-syksy-26')
        self.assertEqual(
            _url_items(page),
            [
                {'title': 'Facebook', 'url': 'https://facebook.com/events/123'},
                {'title': 'Ilmoittautuminen', 'url': 'https://example.com/signup'},
            ],
        )

    def test_update_urls_add_update_remove(self):
        create_payload = {
            **EVENT_PAYLOAD,
            'urls': [
                {'title': 'Facebook', 'url': 'https://facebook.com/events/123'},
                {'title': 'Poistettava', 'url': 'https://example.com/remove-me'},
            ],
        }
        self._post(create_payload)

        update_payload = {
            **EVENT_PAYLOAD,
            'urls': [
                {'title': 'FB', 'url': 'https://facebook.com/events/123'},
                {'title': 'Uusi linkki', 'url': 'https://example.com/new'},
                {'title': None, 'url': 'https://example.com/remove-me'},
            ],
        }
        response = self._post(update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'updated')

        page = EventPage.objects.get(slug='tampere-syksy-26')
        self.assertEqual(
            _url_items(page),
            [
                {'title': 'FB', 'url': 'https://facebook.com/events/123'},
                {'title': 'Uusi linkki', 'url': 'https://example.com/new'},
            ],
        )

    def test_omitting_urls_leaves_existing_links(self):
        self._post(
            {
                **EVENT_PAYLOAD,
                'urls': [{'title': 'Facebook', 'url': 'https://facebook.com/events/123'}],
            }
        )
        response = self._post(EVENT_PAYLOAD)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'unchanged')

        page = EventPage.objects.get(slug='tampere-syksy-26')
        self.assertEqual(
            _url_items(page),
            [{'title': 'Facebook', 'url': 'https://facebook.com/events/123'}],
        )

    def test_unchanged_when_urls_ops_are_no_ops(self):
        payload = {
            **EVENT_PAYLOAD,
            'urls': [{'title': 'Facebook', 'url': 'https://facebook.com/events/123'}],
        }
        self._post(payload)
        page = EventPage.objects.get(slug='tampere-syksy-26')
        revision_count = page.revisions.count()

        response = self._post(
            {
                **payload,
                'urls': [{'title': 'Facebook', 'url': 'https://facebook.com/events/123'}],
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'unchanged')
        page.refresh_from_db()
        self.assertEqual(page.revisions.count(), revision_count)

    def test_url_only_change_returns_updated(self):
        payload = {
            **EVENT_PAYLOAD,
            'urls': [{'title': 'Facebook', 'url': 'https://facebook.com/events/123'}],
        }
        self._post(payload)
        page = EventPage.objects.get(slug='tampere-syksy-26')
        revision_count = page.revisions.count()

        response = self._post(
            {
                **EVENT_PAYLOAD,
                'urls': [{'title': 'FB', 'url': 'https://facebook.com/events/123'}],
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'updated')
        page.refresh_from_db()
        self.assertEqual(page.revisions.count(), revision_count + 1)
        self.assertEqual(
            _url_items(page),
            [{'title': 'FB', 'url': 'https://facebook.com/events/123'}],
        )

    def test_invalid_urls_payload_returns_400(self):
        response = self._post({**EVENT_PAYLOAD, 'urls': [{'url': 'https://example.com/'}]})
        self.assertEqual(response.status_code, 400)
        self.assertIn('urls', response.json())

        response = self._post({**EVENT_PAYLOAD, 'urls': [{'title': 'Bad', 'url': 'not-a-url'}]})
        self.assertEqual(response.status_code, 400)
        self.assertIn('urls', response.json())
