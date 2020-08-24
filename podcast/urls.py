# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.urls import path
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from wagtail.contrib.sitemaps.views import sitemap
from .views import RefreshView

urlpatterns = [
    path('refresh/', RefreshView.as_view(), name='podcast_podcast_modeladmin_refresh')
]