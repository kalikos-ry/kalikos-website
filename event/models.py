from django.db import models
from django.utils import timezone
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail import images
from home.normal_page import NormalPage

class UpcomingEventsBlock(blocks.StaticBlock):
    class Meta:
        template = 'event/events_block.html'
       
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['events'] = EventPage.objects.get_upcoming()[:3]
        context['no_events'] = "Ei tulevia tapahtumia tiedossa nyt..."
        return context
       
class PastEventsBlock(blocks.StaticBlock):
    class Meta:
       template = 'event/events_block.html'

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        context['events'] = EventPage.objects.get_past()[:6]
        context['no_events'] = "Ei menneitä tapahtumia..."
        return context

class EventIndexPage(Page):
    subpage_types=['EventPage']
    title_image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('upcoming_events', UpcomingEventsBlock()),
        ('past_events', PastEventsBlock()),
        ])
        
    content_panels = Page.content_panels + [
        ImageChooserPanel('title_image', classname="full"),
        StreamFieldPanel('body'),
    ]

from wagtail.core.models import PageManager
class EventManager(PageManager):
    def get_upcoming(self):
        return self.get_queryset().exclude(end__lt=timezone.now()).order_by('start')

    def get_past(self):
        return self.get_queryset().exclude(end__gt=timezone.now()).order_by('-start')

class EventPage(Page):
    start = models.DateTimeField("Event start date and time")
    end = models.DateTimeField("Event end date and time")
    intro = models.CharField(max_length=250)
    description = RichTextField(blank=True)
    image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    location = models.CharField(max_length=250)
    location_exact = models.CharField(max_length=500)
    urls = StreamField([
        ('urls', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('url', blocks.URLBlock()),
            ], template="event/urls_block.html"),
        )
    ], blank=True)
    
    objects = EventManager()
    

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
    parent_page_types=['EventIndexPage']