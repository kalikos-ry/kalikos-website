from django.conf import settings
from django.db import transaction
from django.urls import path
from django.utils import timezone
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

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
)


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


def _normalize_value(name, value):
    if name in ('start', 'end', 'go_live_at'):
        if value is None:
            return None
        if timezone.is_naive(value):
            return timezone.make_aware(value)
        return value
    if value is None:
        return ''
    return value


def _values_after_upsert(page, data):
    values = {
        'title': data['title'],
        'intro': data['intro'],
        'location': data['location'],
        'location_exact': data['location_exact'],
        'start': data['start'],
        'end': data['end'],
        'description': data.get('description', page.description),
        'go_live_at': data.get('go_live_at', page.go_live_at),
    }
    return values


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
