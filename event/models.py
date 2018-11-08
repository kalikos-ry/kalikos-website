from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

class EventIndexPage(Page):
    pass

class EventPage(Page):
    start = models.DateTimeField("Event start date and time")
    end = models.DateTimeField("Event end date and time")
    intro = models.CharField(max_length=250)
    description = RichTextField(blank=True)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    location = models.CharField(max_length=250)
    location_exact = models.CharField(max_length=500)
    urls = StreamField([
        ('urls', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('url', blocks.URLBlock()),
            ], template="event/urls_block.html"),
        )
    ], blank=True)
    

    # Editor panels configuration

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('start'),
            FieldPanel('end'),
        ]),
        MultiFieldPanel([
            FieldPanel('location'),
            FieldPanel('location_exact'),
        ]),
        ImageChooserPanel('image'),
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),
        StreamFieldPanel('urls'),
    ]