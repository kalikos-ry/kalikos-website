from django.db import models
from apps.home.normal_page import NormalPage
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtailnews.models import AbstractNewsItem, AbstractNewsItemRevision
from wagtail.fields import RichTextField
from wagtail import blocks
from wagtailnews.decorators import newsindex
from wagtailnews.models import NewsIndexMixin
from wagtail import images

class NewsStructValue(blocks.StructValue):
    def news(self):
        return NewsItem.objects.live()[:self.get('amount')]
        
    def bootstrapcolsm(self):
        return "col-sm-%d" % (12/self.get('amount'))
    
    def news_url(self):
        return NewsIndex.objects.first().url
    
class NewsBlock(blocks.StructBlock):
    amount = blocks.IntegerBlock()
    
    class Meta:
        value_class = NewsStructValue

class NewsItem(AbstractNewsItem):
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=250)
    body = RichTextField()
    image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('image'),
    ]

    def __str__(self):
        return self.title

# This table is used to store revisions of the news items.
class NewsItemRevision(AbstractNewsItemRevision):
    # This is the only field you need to define on this model.
    # It must be a foreign key to your NewsItem model,
    # be named 'newsitem', and have a related_name='revisions'
    newsitem = models.ForeignKey(NewsItem, related_name='revisions', on_delete=models.CASCADE)
    
## TODO: Move to kalikos_site this!
@newsindex
class NewsIndex(NewsIndexMixin, NormalPage):
    newsitem_model = 'NewsItem'
