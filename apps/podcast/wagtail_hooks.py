from django.urls import path
from wagtail import hooks

from .views import RefreshView

#@hooks.register('register_admin_urls')
def register_podcast_admin_url():
  return [
    path('refresh/', RefreshView.as_view(), name='podcast_podcast_modeladmin_refresh')
  ]
