from django.db import models
from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from django import forms
from wagtail import images
from wagtail.images.edit_handlers import ImageChooserPanel
import feedparser

class Podcast(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    feed_url = models.URLField()
    image = models.URLField(null=True)
    
    def __str__(self):
        return self.name
        
    def refresh_episodes(self):
        feed = feedparser.parse(self.feed_url)
        
        for ep in self.episodes.all():
            ep.delete()

        loop_max = len(feed['entries']) # self.max_episodes if len(feed['entries']) > max_episodes else len(feed['entries'])
        
        for i in range(0, loop_max):
            if feed['entries'][i]:
                e = feed['entries'][i]
                ep = Episode()
                ep.podcast = self
                ep.title = e.title
                ep.save()
    
class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name="episodes")
    title = models.CharField(max_length=512)
    description = models.TextField()
    number = models.CharField(max_length=10)
    link = models.URLField()
    date = models.DateField()
    
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
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('podcast', PodcastBlock())
        ], null=True)
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('title_image', classname="full"),
        StreamFieldPanel('body'),
    ]