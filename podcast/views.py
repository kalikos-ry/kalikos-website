from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

class RefreshView(View):
    def get(self, request, *arg, **kwargs):
        return HttpResponse('Hello Refreseh!')