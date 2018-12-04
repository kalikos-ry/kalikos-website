from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail import images

class NormalPage(Page):
    title_image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], blank=True)
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('title_image', classname="full"),
        StreamFieldPanel('body'),
    ]
    