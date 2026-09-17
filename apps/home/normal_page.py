from django.db import models
from django.utils import timezone

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail import images

class KalikosPage(models.Model):
    class Meta:
        abstract = True

    title_image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)

    api_fields = [
        APIField('title_image'),
    ]

class NormalPage(Page, KalikosPage):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)

    api_fields = KalikosPage.api_fields + [
        APIField('body'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('title_image', classname="full"),
        FieldPanel('body'),
    ]
    
