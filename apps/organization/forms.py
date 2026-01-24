from django import forms
from django_recaptcha.fields import ReCaptchaField
from .membra import MembraClient

class JoinOrganizationForm(forms.Form):
    first_name = forms.CharField(max_length=255, label='Etunimi')
    last_name = forms.CharField(max_length=255, label='Sukunimi')
    email = forms.EmailField(label='Sähköpostiosoite')
    city = forms.CharField(max_length=255, label='Kotipaikka')
    
    captcha = ReCaptchaField()
    
    def save(self):
        c = MembraClient()
        member = c.add_member(self.cleaned_data)
        return member