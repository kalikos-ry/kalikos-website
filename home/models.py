from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail import images

from event.models import EventPage
from .normal_page import NormalPage
from news.models import NewsItem, NewsIndex
from event.models import EventsBlock

from kalikos_site.models import BrandingSettings
from news.models import NewsBlock

class HomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('news', NewsBlock(template='home/blocks/news.html')),
        ('events', EventsBlock(template='home/blocks/events.html')),
        ],blank=True)

    text_image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    title_text = models.TextField()
    title_subtext = models.TextField()
    #body = RichTextField(blank=True)
    # Editor panels configuration

    content_panels = Page.content_panels + [
        ImageChooserPanel('text_image', classname="full"),
        FieldPanel('title_text', classname="full"),
        FieldPanel('title_subtext', classname="full"),
        StreamFieldPanel('body', classname="full"),
        #FieldPanel('body', classname="full"),
    ]
    
    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['events'] = EventPage.objects.get_upcoming()[:3]
        context['menuitems'] = self.get_children().filter(live=True, show_in_menus=True)
        return context

class ContactsPage(NormalPage):
    address = models.TextField()
    
    @property
    def email(self):
        return BrandingSettings.objects.first().email
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('title_image', classname="full"),
        FieldPanel('address', classname="full"),
    ]