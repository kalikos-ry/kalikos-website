from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.management import call_command
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.viewsets.model import ModelViewSet

class RefreshView(View):
    def get(self, request, *arg, **kwargs):
        result = call_command('fetch_podcast_episodes')
        return HttpResponse('OK')
    
class PodcastChooserViewSet(ChooserViewSet):
    # The model can be specified as either the model class or an "app_label.model_name" string;
    # using a string avoids circular imports when accessing the StreamField block class (see below)
    model = 'podcast.Podcast'

podcast_chooser_viewset = PodcastChooserViewSet("podcast_chooser")
