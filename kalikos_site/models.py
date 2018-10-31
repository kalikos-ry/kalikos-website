from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting

@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(blank=True,
        help_text='Your Facebook page URL')
    mewe = models.URLField(blank=True,
        help_text='Your MeWe page URL')
    youtube = models.URLField(blank=True,
        help_text='Your YouTube channel or user account URL')