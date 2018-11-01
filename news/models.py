from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtailnews.models import AbstractNewsItem, AbstractNewsItemRevision
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from home.models import NormalPage
from wagtailnews.decorators import newsindex
from wagtailnews.models import NewsIndexMixin


class NewsItem(AbstractNewsItem):
    title = models.CharField(max_length=100)
    body = RichTextField()
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='+', null=True)

    panels = [
        FieldPanel('title'),
        FieldPanel('body'),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return self.title

# This table is used to store revisions of the news items.
class NewsItemRevision(AbstractNewsItemRevision):
    # This is the only field you need to define on this model.
    # It must be a foreign key to your NewsItem model,
    # be named 'newsitem', and have a related_name='revisions'
    newsitem = models.ForeignKey(NewsItem, related_name='revisions')
    
@newsindex
class NewsIndex(NewsIndexMixin, NormalPage):
    newsitem_model = 'NewsItem'