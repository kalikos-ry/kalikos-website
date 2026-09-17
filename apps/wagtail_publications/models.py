from django.db import models
from django.utils import timezone

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.api import APIField
from wagtail import images
from apps.home.normal_page import NormalPage
from apps.home.models import SnipcartSettings

import requests

WEIGHT_TYPES = (
    (200, 'lehti'),
    (1500, 'kirja'),
    )

class PublicationIndexPage(NormalPage):
    def get_publications(self):
        return PublicationPage.objects.all()
    subpage_types = ['PublicationPage']

class PublicationPage(Page):
    image = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    description = RichTextField(blank=True)
    
    sku = models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    pdf_price = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    snipcart_digital_id = models.UUIDField(blank=True, null=True)
    weight = models.IntegerField(choices=WEIGHT_TYPES, blank=True, null=True)

    api_fields = [
        APIField('image'),
        APIField('description'),
        APIField('sku'),
        APIField('price'),
        APIField('pdf_price'),
        APIField('weight'),
        APIField('snipcart_digital_id'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('image', classname="full"),
        FieldPanel('description', classname="full"),
        FieldPanel('sku', classname="full"),
        FieldRowPanel([
            FieldPanel('price', classname="col12"),
            FieldPanel('pdf_price', classname="col6"),
            FieldPanel('snipcart_digital_id', classname="col6"),
            FieldPanel('weight', classname="col6"),
            ])
    ]
    parent_page_types = ['PublicationIndexPage']
    subpage_types = ['IssuePage']
    
    @property
    def shop_title(self):
        return "%s" % (self.title)
    
    def get_issues(self):
        return IssuePage.objects.live().descendant_of(self).order_by('-publication_date')
        
    def get_latest_issues(self):
        return IssuePage.objects.live().descendant_of(self).order_by('-publication_date')[:3]
        
    def get_context(self, request):
        context = super().get_context(request)
        api_key = SnipcartSettings.load(request_or_site=request).secret_api_key
        stocks = {}
        if api_key:
            headers = { 'Accept' : 'application/json' }
            products = requests.get('https://app.snipcart.com/api/products', params=(('limit', 100),), auth=(api_key,''), headers=headers)
            if products.status_code == 200:
                for p in products.json()['items']:
                    stocks[p['userDefinedId']] = {
                        'stock': p['stock'] if 'stock' in p else 0,
                        'allowOutOfStockPurchases': p['allowOutOfStockPurchases'] if 'allowOutOfStockPurchases' in p else False
                        }
            discounts = requests.get('https://app.snipcart.com/api/discounts', params=(('limit', 100),), auth=(api_key,''), headers=headers)
            if discounts.status_code == 200:
                for d in discounts.json():
                    if d['archived'] == False and d['trigger'] == 'Product' and d['productIds'].endswith('-pdf') and d['type'] == "RateOnItems" and d['rate'] == 100:
                        stocks[d['itemId']]['pdfDiscount'] = True
        if stocks:
            context['stocks'] = stocks
        return context

class IssuePage(Page):
    publication = models.ForeignKey(PublicationPage, on_delete=models.PROTECT)
    contents = RichTextField(blank=True)
    cover = models.ForeignKey(images.get_image_model_string(), on_delete=models.SET_NULL, related_name='+', null=True)
    publication_date = models.DateField(default=timezone.now)
    number = models.IntegerField()
    
    price = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    pdf_price = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    snipcart_digital_id = models.UUIDField(blank=True, null=True)
    weight = models.IntegerField(choices=WEIGHT_TYPES, blank=True, null=True)
    
    @property
    def sku(self):
        return "%s-%s" % (self.publication.sku, self.number)
        
    @property
    def shop_title(self):
        return "%s #%s" % (self.publication.title, self.number)
    
    def url(self):
        return self.publication.url + "#" + self.title

    api_fields = [
        APIField('publication'),
        APIField('contents'),
        APIField('cover'),
        APIField('publication_date'),
        APIField('number'),
        APIField('price'),
        APIField('pdf_price'),
        APIField('weight'),
        APIField('sku'),
        APIField('snipcart_digital_id'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('publication', classname="full"),
        FieldPanel('number', classname="full"),
        FieldPanel('publication_date', classname="full"),
        FieldPanel('cover', classname="full"),
        FieldPanel('contents', classname="full"),
        FieldRowPanel([
            FieldPanel('price', classname="col12"),
            FieldPanel('pdf_price', classname="col6"),
            FieldPanel('snipcart_digital_id', classname="col6"),
            FieldPanel('weight', classname="col6"),
            ])
    ]
    parent_page_types = ['PublicationPage']
