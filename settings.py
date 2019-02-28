# -*- coding: utf-8 -*-
import os

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-google-analytics',
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
    #'wagtail.contrib.routable_page',
    
    'kalikos_site',
    'home',
    'event',
    'news',
    'wagtail_publications',
    
    'sass_processor',
])

USE_TZ = True

STATICFILES_FINDERS.extend([
    'compressor.finders.CompressorFinder',
    ])
    
LANGUAGE_CODE='fi'
    
TEMPLATES[0]['OPTIONS']['context_processors'].extend([
                'kalikos_site.context_processors.image_tracking',
                'wagtail.contrib.settings.context_processors.settings',
                'wagtailmenus.context_processors.wagtailmenus',
                ])

WAGTAILIMAGES_IMAGE_MODEL = 'kalikos_site.KalikosImage'