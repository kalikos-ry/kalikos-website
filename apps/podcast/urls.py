# -*- coding: utf-8 -*-
from django.urls import path
from .views import RefreshView

urlpatterns = [
    path('refresh/', RefreshView.as_view(), name='podcast_podcast_modeladmin_refresh')
]