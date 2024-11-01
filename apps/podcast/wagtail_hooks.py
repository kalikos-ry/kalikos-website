from django.urls import path
from wagtail import hooks

from .views import RefreshView, podcast_chooser_viewset
from .models import podcast_viewset

@hooks.register("register_admin_viewset")
def register_viewset():
    return podcast_viewset

@hooks.register("register_admin_viewset")
def register_viewset():
    return podcast_chooser_viewset

@hooks.register('register_admin_urls')
def register_podcast_admin_url():
  return [
    path('podcasts/refresh/', RefreshView.as_view(), name='podcast_podcast_modeladmin_refresh')
  ]
