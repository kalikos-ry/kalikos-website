import os
from io import BytesIO
from urllib.parse import unquote, urlparse

import requests
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import transaction
from django.urls import path
from django.utils import timezone
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.images import get_image_model

from apps.event.models import EventIndexPage, EventPage

COMPARE_FIELDS = (
    'title',
    'intro',
    'description',
    'location',
    'location_exact',
    'start',
    'end',
    'go_live_at',
    'image',
)

CONTENT_TYPE_EXTENSIONS = {
    'image/jpeg': '.jpg',
    'image/jpg': '.jpg',
    'image/png': '.png',
    'image/gif': '.gif',
    'image/webp': '.webp',
}


class UpsertEventSerializer(serializers.Serializer):
    slug = serializers.SlugField(max_length=255)
    title = serializers.CharField(max_length=255)
    intro = serializers.CharField(max_length=250)
    description = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(max_length=250)
    location_exact = serializers.CharField(max_length=500)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    go_live_at = serializers.DateTimeField(required=False, allow_null=True)
    image = serializers.URLField()


def _normalize_value(name, value):
    if name in ('start', 'end', 'go_live_at'):
        if value is None:
            return None
        if timezone.is_naive(value):
            return timezone.make_aware(value)
        return value
    if name == 'image':
        return value
    if value is None:
        return ''
    return value


def _values_after_upsert(page, data):
    return {
        'title': data['title'],
        'intro': data['intro'],
        'location': data['location'],
        'location_exact': data['location_exact'],
        'start': data['start'],
        'end': data['end'],
        'description': data.get('description', page.description),
        'go_live_at': data.get('go_live_at', page.go_live_at),
        'image': data['image'].pk,
    }


def _current_values(page):
    return {
        'title': page.title,
        'intro': page.intro,
        'description': page.description,
        'location': page.location,
        'location_exact': page.location_exact,
        'start': page.start,
        'end': page.end,
        'go_live_at': page.go_live_at,
        'image': page.image_id,
    }


def _fields_changed(page, data):
    incoming = _values_after_upsert(page, data)
    current = _current_values(page)
    for name in COMPARE_FIELDS:
        if _normalize_value(name, incoming[name]) != _normalize_value(name, current[name]):
            return True
    return False


def _apply_fields(page, data):
    page.title = data['title']
    page.draft_title = data['title']
    page.intro = data['intro']
    page.location = data['location']
    page.location_exact = data['location_exact']
    page.start = data['start']
    page.end = data['end']
    page.image = data['image']
    if 'description' in data:
        page.description = data['description']
    if 'go_live_at' in data:
        page.go_live_at = data['go_live_at']


def _response_payload(page, status):
    return {
        'status': status,
        'page_id': page.id,
        'slug': page.slug,
        'url': page.get_url(),
    }


def _filename_from_slug(slug, url, response):
    path = unquote(urlparse(url).path)
    name = os.path.basename(path)
    if name and '.' in name:
        return name
    content_type = response.headers.get('Content-Type', '').split(';')[0].strip().lower()
    ext = CONTENT_TYPE_EXTENSIONS.get(content_type, '.jpg')
    return f'event-image-{slug}{ext}'


def _get_or_create_image(slug, url):
    image_model = get_image_model()
    existing = image_model.objects.filter(title=slug).first()
    if existing:
        return existing

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise serializers.ValidationError({'image': f'Could not fetch image: {exc}'}) from exc

    filename = _filename_from_slug(slug, url, response)
    try:
        image = image_model(
            title=slug,
            file=ImageFile(BytesIO(response.content), name=filename),
        )
        image.save()
    except Exception as exc:
        raise serializers.ValidationError({'image': f'Could not save image: {exc}'}) from exc
    return image


class UpsertEvent(APIView):
    @classmethod
    def get_urlpatterns(cls):
        return [
            path('', cls.as_view(), name='upsert_event'),
        ]

    def _authorized(self, request):
        token = settings.EVENT_API_TOKEN
        if not token:
            return False
        return request.headers.get('X-ApiKey') == token

    def post(self, request):
        if not self._authorized(request):
            return Response({'detail': 'Unauthorized'}, status=401)

        serializer = UpsertEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        parent = EventIndexPage.objects.live().first()
        if parent is None:
            return Response({'detail': 'No live EventIndexPage found'}, status=400)

        slug = data['slug']

        try:
            data['image'] = _get_or_create_image(slug, data['image'])
        except serializers.ValidationError as exc:
            return Response(exc.detail, status=400)

        with transaction.atomic():
            page = EventPage.objects.child_of(parent).filter(slug=slug).first()
            if page is None:
                page = EventPage(
                    title=data['title'],
                    draft_title=data['title'],
                    slug=slug,
                    intro=data['intro'],
                    description=data.get('description', ''),
                    location=data['location'],
                    location_exact=data['location_exact'],
                    start=data['start'],
                    end=data['end'],
                    image=data['image'],
                )
                if 'go_live_at' in data:
                    page.go_live_at = data['go_live_at']
                parent.add_child(instance=page)
                page.save_revision().publish()
                return Response(_response_payload(page, 'created'))

            if not _fields_changed(page, data):
                return Response(_response_payload(page, 'unchanged'))

            _apply_fields(page, data)
            page.save_revision().publish()
            return Response(_response_payload(page, 'updated'))
