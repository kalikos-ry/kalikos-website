from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.core.management import call_command

class RefreshView(View):
    def get(self, request, *arg, **kwargs):
        result = call_command('fetch_podcast_episodes')
        return HttpResponse('OK')