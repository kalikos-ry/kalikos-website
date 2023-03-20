from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.panels import FieldPanel
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail import images

@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(blank=True,
        help_text='Your Facebook page URL')
    mewe = models.URLField(blank=True,
        help_text='Your MeWe page URL')
    youtube = models.URLField(blank=True,
        help_text='Your YouTube channel or user account URL')
    discord = models.URLField(blank=True,
        help_text='Your Discord invite link')
        
@register_setting
class BrandingSettings(BaseSetting):
    footer_logo = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    header_logo = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    email = models.EmailField()
    
    panels = [
        FieldPanel('header_logo'),
        FieldPanel('footer_logo'),
        ]

class KalikosImage(AbstractImage):
    attribution = models.CharField(max_length=500, blank=True)
    attribution_url = models.URLField(blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        'attribution', 'attribution_url'
    )

class KalikosRendition(AbstractRendition):
    image = models.ForeignKey(KalikosImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
