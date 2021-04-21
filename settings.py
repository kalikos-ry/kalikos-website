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
    'organization',
    
    'django_social_share',
    'puput',
    'colorful',
    'captcha',
    'bootstrap4',

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
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', 'invalid')
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', 'invalid')
MEMBRA_API_TOKEN = os.environ.get('MEMBRA_API_TOKEN')

PUPUT_AS_PLUGIN = True

if DEBUG:
    ALLOWED_HOSTS = [ '347caa2e67f24f97b79f80ef2eeaaa1c.vfs.cloud9.eu-west-1.amazonaws.com', '*' ]
    CSRF_TRUSTED_ORIGINS = [ '*.amazon.com' ]
    CSRF_COOKIE_SAMESITE = 'lax'
    SESSION_COOKIE_SAMESITE = 'lax'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'ALLOW-FROM https://347caa2e67f24f97b79f80ef2eeaaa1c.vfs.cloud9.eu-west-1.amazonaws.com'