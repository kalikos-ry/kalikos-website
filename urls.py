# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.urls import path
from aldryn_django.utils import i18n_patterns
import aldryn_addons.urls
from wagtail.contrib.sitemaps.views import sitemap
from puput.views import *
from puput.feeds import BlogPageFeed
from podcast import urls as podcast_urls

# Puput urls are here manually as the original entry_page_serve_slug
# is not compatible with wagtailnews
puput_urls = [
    path(
        route='entry_page/<entry_page_id>/update_comments/',
        view=EntryPageUpdateCommentsView.as_view(),
        name='entry_page_update_comments'
    ),
    path(
        route='<path:blog_path>/_<int:year>/<int:month>/<int:day>/<str:slug>/',
        view=EntryPageServe.as_view(),
        name='entry_page_serve_slug'
    ),
    path(
        route='<int:year>/<int:month>/<int:day>/<str:slug>/',
        view=EntryPageServe.as_view(),
        name='entry_page_serve'
    ),
    path(
        route='<path:blog_path>/feed/',
        view=BlogPageFeed(),
        name='blog_page_feed_slug'
    ),
    path(
        route='feed/',
        view=BlogPageFeed(),
        name='blog_page_feed'
    ),
]

urlpatterns = [
    # add your own patterns here
    url('^sitemap\.xml$', sitemap),
    url('podcast/', include(podcast_urls)),
] + puput_urls + aldryn_addons.urls.patterns() + [
] + i18n_patterns(
    # add your own i18n patterns here
    *aldryn_addons.urls.i18n_patterns()  # MUST be the last entry!
)
