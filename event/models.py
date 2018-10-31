from django.db import models

# Create your models here.

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

# Create your models here.

class EventPage(Page):
    start = models.DateTimeField("Event start date and time")
    end = models.DateTimeField("Event end date and time")
    intro = models.CharField(max_length=250)
    description = RichTextField(blank=True)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)

    # Editor panels configuration

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('start'),
            FieldPanel('end'),
        ]),
        ImageChooserPanel('image'),
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),
    ]