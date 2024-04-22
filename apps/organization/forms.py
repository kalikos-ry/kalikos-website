from django import forms
from django.utils import timezone
from apiclient import APIClient, HeaderAuthentication, JsonResponseHandler
from captcha.fields import ReCaptchaField
from django.conf import settings

class MembraClient(APIClient):
    def __init__(self, *args, **kwargs):
        kwargs['authentication_method'] = HeaderAuthentication(
            token=settings.MEMBRA_API_TOKEN,
            parameter="X-Api-Key",
            scheme=None,
            )
        kwargs['response_handler'] = JsonResponseHandler
        super().__init__(*args, **kwargs)
        
    def add_member(self, data):
        url = "https://api.membra.fi/v2/member"
        mdata = {
            'mem_firstname': data['first_name'],
            'mem_lastname': data['last_name'],
            'mem_email': data['email'],
            'mef_id': '1',
            'mem_street': data['city'],
            'mem_city': '-',
            'mem_sex': '-',
            'mem_accept_email_invoice': 1,
            'mes_entrydate': timezone.now().strftime('%Y-%m-%d'),
            'mes_status': 5, # 5 = applicant
        }
        result = self.post(url, data=mdata)
        if (result['http_status'] == 200):
            return {
                'id': result['data'],
                'name': data['first_name'] + ' ' + data['last_name'],
                'email': data['email'],
            }
        raise Exception("Failed to add member, contact support")

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