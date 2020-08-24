from django.contrib import admin
from .models import Podcast, Episode
from wagtail.contrib.modeladmin.helpers import ButtonHelper

from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    modeladmin_register,
)

class PodcastButtonHelper(ButtonHelper):
    def refresh_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.add_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': self.url_helper.get_action_url('refresh'),
            'label': 'Refresh',
            'classname': cn,
            'title': 'Refresh %s' % self.verbose_name,
        }

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
    button_helper_class = PodcastButtonHelper

modeladmin_register(PodcastAdmin) 