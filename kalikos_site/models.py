from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel

@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(blank=True,
        help_text='Your Facebook page URL')
    mewe = models.URLField(blank=True,
        help_text='Your MeWe page URL')
    youtube = models.URLField(blank=True,
        help_text='Your YouTube channel or user account URL')
        
@register_setting
class BrandingSettings(BaseSetting):
    footer_logo = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    header_logo = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    email = models.EmailField()
    
    panels = [
        ImageChooserPanel('header_logo'),
        ImageChooserPanel('footer_logo'),
        ]