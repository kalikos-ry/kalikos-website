# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.urls import path
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from wagtail.contrib.sitemaps.views import sitemap
from podcast import urls as podcast_urls

urlpatterns = [
    # add your own patterns here
    url('^sitemap\.xml$', sitemap),
    url('podcast/', include(podcast_urls)),
] + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
