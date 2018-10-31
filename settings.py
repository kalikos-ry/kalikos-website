# -*- coding: utf-8 -*-
import os

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-wagtail',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())


# all django settings can be altered here

INSTALLED_APPS.extend([
    # add your project specific apps here
    
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'wagtailmenus',
    
    'kalikos_site',
    'home',
    'event',
    
    'sass_processor',
])

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')

STATICFILES_FINDERS.extend([
    'compressor.finders.CompressorFinder',
    ])
    
LANGUAGE_CODE='fi'
    
TEMPLATES[0]['OPTIONS']['context_processors'].extend([
                'wagtail.contrib.settings.context_processors.settings',
                'wagtailmenus.context_processors.wagtailmenus',
                ])