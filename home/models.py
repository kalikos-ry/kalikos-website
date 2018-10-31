from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from event.models import EventPage

# Create your models here.

class HomePage(Page):
    body = RichTextField(blank=True)

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
    
    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['events'] = EventPage.objects.exclude(end__lt=timezone.now()).order_by('start')
        context['menuitems'] = self.get_children().filter(live=True, show_in_menus=True)
        return context

class NormalPage(Page):
    title_image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('title_image', classname="full"),
    ]
    
class ContactsPage(NormalPage):
    address = models.TextField()
    
    content_panels = NormalPage.content_panels + [
        FieldPanel('address', classname="full"),
    ]