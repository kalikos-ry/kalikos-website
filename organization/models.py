from django.db import models
from django.shortcuts import render

from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from home.normal_page import NormalPage, KalikosPage
from .forms import JoinOrganizationForm

class JoinOrganizationPage(Page, KalikosPage):
    thank_you = RichTextField(blank=True)
    form_instructions = RichTextField(blank=True)
    email_help_text = models.CharField(max_length=1024)
    submit_button_text = models.CharField(max_length=255)
    
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], blank=True)
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('title_image', classname="full"),
        StreamFieldPanel('body'),
        FieldPanel('thank_you'),
        FieldPanel('form_instructions'),
        FieldPanel('email_help_text'),
        FieldPanel('submit_button_text'),
    ]
    
    
    def serve(self, request):
        form = JoinOrganizationForm(request.POST)
        if form.is_valid():
            member = form.save()
            return render(request, 'organization/join_form.html', {
                'page': self,
                'member': member
            })
            
        form = JoinOrganizationForm()
        form.fields['email'].help_text = self.email_help_text
        
        return render(request, 'organization/join_form.html', {
            'page': self,
            'form': form
        })