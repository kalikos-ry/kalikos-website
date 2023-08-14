# -*- coding: utf-8 -*-
from django.urls import re_path, include
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from wagtail.contrib.sitemaps.views import sitemap
from podcast import urls as podcast_urls

urlpatterns = [
    # add your own patterns here
    re_path('^sitemap\.xml$', sitemap),
    re_path('podcast/', include(podcast_urls)),
] + aldryn_addons.urls.patterns() + [
] + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
