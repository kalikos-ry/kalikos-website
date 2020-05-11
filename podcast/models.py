from django.db import models
from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from django import forms
from wagtail import images
from wagtail.images.edit_handlers import ImageChooserPanel

class Podcast(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    feed_url = models.URLField()
    
    def __str__(self):
        return self.name
        
    def refresh_episodes(self):
        pass
    
class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name="episodes")
    title = models.CharField(max_length=512)
    description = models.TextField()
    number = models.CharField(max_length=10)
    url = models.URLField()
    
class PodcastChooserBlock(blocks.ChooserBlock):
    target_model=Podcast
    widget=forms.Select

class PodcastBlock(blocks.StructBlock):
    podcast = PodcastChooserBlock()
    description = blocks.RichTextBlock()
    
    class Meta:
        template = 'podcast/podcast_block.html'
    
class PodcastPage(Page):
    title_image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('podcast', PodcastBlock())
        ], null=True)
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('title_image', classname="full"),
        StreamFieldPanel('body'),
    ]