from django.conf import settings

def image_tracking(request):
    return { 'rendered_images': {} }

def gtag_id(request):
    return { 'GTAG_ID': settings.GTAG_ID }