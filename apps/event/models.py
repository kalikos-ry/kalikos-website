from django.db import models
from django.utils import timezone
from wagtail.models import Page, PageManager
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail import images

class EventStructValue(blocks.StructValue):
    def events(self):
        return EventPage.objects.get_events(self.get('event_type'))[:(int)(self.get('default_amount'))]

class EventsBlock(blocks.StructBlock):
    event_type = blocks.ChoiceBlock(choices=(('get_past', "Menneet"), ('get_upcoming', "Tulevat")))
    alt_text = blocks.RichTextBlock()
    default_amount = blocks.IntegerBlock(default=3)
    # load_all_allow = blocks.BooleanBlock(default=False, required=False)
    # load_all_text = blocks.RichTextBlock(required=False)

    class Meta:
        template = 'event/events_block.html'
        value_class = EventStructValue

class EventIndexPage(Page):
    subpage_types=['EventPage']
    title_image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('events', EventsBlock()),
        ], use_json_field=True)

    api_fields = [
        APIField('title_image'),
        APIField('body'),
    ]
        
    content_panels = Page.content_panels + [
        FieldPanel('title_image', classname="full"),
        FieldPanel('body'),
    ]

class EventManager(PageManager):
    def get_upcoming(self):
        return self.get_queryset().exclude(end__lt=timezone.now()).order_by('start')

    def get_past(self):
        return self.get_queryset().exclude(end__gt=timezone.now()).order_by('-start')

    def get_events(self, events_type):
        return getattr(self,events_type)()

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
    ], use_json_field=True, blank=True)
    
    objects = EventManager()

    api_fields = [
        APIField('start'),
        APIField('end'),
        APIField('intro'),
        APIField('description'),
        APIField('image'),
        APIField('location'),
        APIField('location_exact'),
        APIField('urls'),
    ]

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
        FieldPanel('image'),
        FieldPanel('intro', classname="full"),
        FieldPanel('description', classname="full"),
        FieldPanel('urls'),
    ]
    parent_page_types=['EventIndexPage']
