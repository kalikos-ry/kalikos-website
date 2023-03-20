# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    wagtail_site_name = forms.CharField(
        'Wagtail Sitename',
        required=True,
        initial='My Example Site',
    )

    def to_settings(self, data, settings):
        settings['INSTALLED_APPS'].extend([
            'wagtail.contrib.forms',
            'wagtail.contrib.redirects',
            'wagtail.contrib.modeladmin',
            'wagtail.embeds',
            'wagtail.sites',
            'wagtail.users',
            'wagtail.snippets',
            'wagtail.documents',
            'wagtail.images',
            'wagtail.search',
            'wagtail.admin',
            'wagtail.core',

            'modelcluster',
            'taggit',
        ])
        settings['MIDDLEWARE'].extend([
            'wagtail.contrib.legacy.sitemiddleware.SiteMiddleware',
            'wagtail.contrib.redirects.middleware.RedirectMiddleware',
        ])
        # admin and cms urls need to be first, since we're overriding the
        # default admin.
        # These are non-translatable URLs
        # see: https://docs.wagtail.io/en/stable/advanced_topics/i18n.html#adding-a-language-prefix-to-urls
        settings['ADDON_URLS'].insert(
            0,
            'aldryn_wagtail.urls',
        )
        settings['ADDON_URLS_I18N_LAST'] = 'aldryn_wagtail.page_urls'
        settings['WAGTAIL_SITE_NAME'] = data['wagtail_site_name']

        return settings
