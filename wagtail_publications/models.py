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
    
    def get_issues(self):
        return IssuePage.objects.live().descendant_of(self).order_by('-publication_date')
        
    def get_latest_issues(self):
        return IssuePage.objects.live().descendant_of(self).order_by('-publication_date')[:3]

class IssuePage(Page):
    publication = models.ForeignKey(PublicationPage, on_delete=models.CASCADE)
    contents = RichTextField(blank=True)
    cover = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)
    publication_date = models.DateField(default=timezone.now)
    number = models.IntegerField()
    
    def url(self):
        return self.publication.url + "#" + self.title
    
    content_panels = Page.content_panels + [
        FieldPanel('publication', classname="full"),
        FieldPanel('number', classname="full"),
        FieldPanel('publication_date', classname="full"),
        ImageChooserPanel('cover', classname="full"),
        FieldPanel('contents', classname="full"),
    ]