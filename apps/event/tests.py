from datetime import datetime
from zoneinfo import ZoneInfo

from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from wagtail.models import Page

from apps.event.models import EventIndexPage, EventPage
from apps.home.models import HomePage

HELSINKI = ZoneInfo('Europe/Helsinki')

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
}


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
