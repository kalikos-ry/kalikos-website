from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from home.normal_page import NormalPage

class PublicationIndexPage(NormalPage):
    def get_publications(self):
        return PublicationPage.objects.all()

class PublicationPage(Page):
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    description = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('image', classname="full"),
        FieldPanel('description', classname="full"),
    ]

class IssuePage(Page):
    publication = models.ForeignKey(PublicationPage, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    contents = RichTextField(blank=True)
    cover = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    publication_date = models.DateField(default=timezone.now())
    
    content_panels = Page.content_panels + [
        FieldPanel('name', classname="full"),
        ImageChooserPanel('cover', classname="full"),
        FieldPanel('contents', classname="full"),
    ]