from django.contrib import admin
from .models import Podcast, Episode

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)

class PodcastAdmin(ModelAdmin):
    """Podcast admin."""

    model = Podcast
    menu_label = "Podcasts"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "url",)
    search_fields = ("name",)

modeladmin_register(PodcastAdmin) 