from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel

# Create your models here.

class HomePage(Page):
    body = RichTextField(blank=True)

    # Editor panels configuration

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
