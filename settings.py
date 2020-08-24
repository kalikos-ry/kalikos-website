# -*- coding: utf-8 -*-
import os

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-sitemap',
    'aldryn-wagtail',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())

# all django settings can be altered here

INSTALLED_APPS.extend([
    # add your project specific apps here
    'wagtail.contrib.settings',
    'wagtailmenus',
    'wagtailnews',
    "wagtail.contrib.routable_page",
    #'wagtail.contrib.wagtailroutablepage',
    
    'kalikos_site',
    'home',
    'event',
    'news',
    'podcast',
    'wagtail_publications',
    
    'django_social_share',
    'puput',
    'colorful',

    'sass_processor',
])

USE_TZ = True
TIME_ZONE = 'Europe/Helsinki'

STATICFILES_FINDERS.extend([
    'compressor.finders.CompressorFinder',
    ])
    
LANGUAGE_CODE='fi'

TEMPLATES[0]['OPTIONS']['context_processors'].extend([
                'kalikos_site.context_processors.image_tracking',
                'wagtail.contrib.settings.context_processors.settings',
                'wagtailmenus.context_processors.wagtailmenus',
                'aldryn_snake.template_api.template_processor'
                ])

WAGTAILIMAGES_IMAGE_MODEL = 'kalikos_site.KalikosImage'

# Do this like this until there is new aldryn_google_analytics
INSTALLED_APPS.extend(['aldryn_google_analytics'])
GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID')

PUPUT_AS_PLUGIN = True
