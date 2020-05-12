# -*- coding: utf-8 -*-
from aldryn_client import forms
import re


class GoogleAnalyticsIDField(forms.CharField):

    GOOGLE_ANALYTICS_ID_FORMAT = re.compile(r'^UA-\d+(-\d+)?$')

    def clean(self, value):
        value = super(GoogleAnalyticsIDField, self).clean(value.strip())
        if not self.GOOGLE_ANALYTICS_ID_FORMAT.match(value):
            raise forms.ValidationError('Invalid format. Google Analytics site tracking ID format is: UA-XXXXXX-YY.')
        return value


class Form(forms.BaseForm):
    google_analytics_id = GoogleAnalyticsIDField('Tracking ID', max_length=50)
    # TODO: add description (not supported by forms yet):
    # https://developers.google.com/analytics/devguides/collection/upgrade/guide#transfer
    use_universal_analytics = forms.CheckboxField('Use Universal Analytics', required=False)
    # https://developers.google.com/analytics/devguides/collection/analyticsjs/user-id?hl=en
    track_individuals = forms.CheckboxField('Track individual logged in users (universal only)', required=False)

    def clean(self):
        super(Form, self).clean()
        if self.cleaned_data['track_individuals'] and not self.cleaned_data['use_universal_analytics']:
            self.errors['track_individuals'] = "Individual user tracking only works in with Universal Analytics."

    def to_settings(self, data, settings):
        settings['GOOGLE_ANALYTICS_ID'] = data['google_analytics_id']
        settings['GOOGLE_ANALYTICS_USE_UNIVERSAL'] = data['use_universal_analytics']
        settings['GOOGLE_ANALYTICS_TRACK_INDIVIDUALS'] = data['track_individuals']
        settings['INSTALLED_APPS'].append('aldryn_google_analytics')

        # aldryn-snake is configured by aldryn-django-cms
        return settings
