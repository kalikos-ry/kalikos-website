from django.db import models
from wagtail.models import Page
from wagtail import blocks
from wagtail import hooks
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.admin.viewsets.model import ModelViewSet
from django import forms
from wagtail import images
import feedparser
from .blocks import PodcastChooserBlock

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
    
    class Meta:
        ordering = ['-date']
    
# This is here because of the circular import
class PodcastViewSet(ModelViewSet):
    model = Podcast
    form_fields = ["name", "url", "feed_url", "image"]
    icon = "user"
    add_to_admin_menu = True
    copy_view_enabled = False
    inspect_view_enabled = True

podcast_viewset = PodcastViewSet("podcast")

class PodcastPage(Page):
    title_image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('podcast', PodcastChooserBlock(template='podcast/podcast_block.html')),
        ], use_json_field=True, null=True)

    api_fields = [
        APIField('title_image'),
        APIField('body'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('title_image', classname="full"),
        FieldPanel('body'),
    ]