from django.db import models
from django.utils import timezone

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail import images
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting

from .normal_page import NormalPage
from apps.event.models import EventsBlock

from apps.kalikos_site.models import BrandingSettings
from apps.news.models import NewsBlock

@register_setting
class SnipcartSettings(BaseGenericSetting):
    api_key = models.CharField(
        max_length=255,
        help_text='Your Snipcart public API key'
    )
    secret_api_key = models.CharField(
        max_length=255,
        help_text='Your Snipcart secret API key',
        null=True,
        blank=True
    )
    member_discount_name = models.CharField(
        max_length=255,
        help_text='The name of the discount code for members',
        null=True,
        blank=True
    )

class HomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('news', NewsBlock(template='home/blocks/news.html')),
        ('events', EventsBlock(template='home/blocks/events.html')),
        ],use_json_field=True, blank=True)

    text_image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    title_text = models.TextField()
    title_subtext = models.TextField()
    #body = RichTextField(blank=True)
    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('text_image', classname="full"),
        FieldPanel('title_text', classname="full"),
        FieldPanel('title_subtext', classname="full"),
        FieldPanel('body', classname="full"),
        #FieldPanel('body', classname="full"),
    ]

class ContactsPage(NormalPage):
    address = models.TextField()
    
    @property
    def email(self):
        return BrandingSettings.objects.first().email
    
    content_panels = Page.content_panels + [
        FieldPanel('title_image', classname="full"),
        FieldPanel('address', classname="full"),
    ]
