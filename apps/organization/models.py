
from django.shortcuts import render

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from apps.home.normal_page import NormalPage, KalikosPage
from .forms import JoinOrganizationForm
from django.db import models

class JoinOrganizationPage(Page, KalikosPage):
    thank_you = RichTextField(blank=True)
    form_instructions = RichTextField(blank=True)
    email_help_text = models.CharField(max_length=1024)
    city_help_text = models.CharField(max_length=1024)
    submit_button_text = models.CharField(max_length=255)
    
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title", template='home/blocks/heading.html')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('title_image', classname="full"),
        FieldPanel('body'),
        FieldPanel('thank_you'),
        FieldPanel('form_instructions'),
        FieldPanel('email_help_text'),
        FieldPanel('city_help_text'),
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
        form.fields['city'].help_text = self.city_help_text
        
        return render(request, 'organization/join_form.html', {
            'page': self,
            'form': form
        })
