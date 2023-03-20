from django import forms
from django.utils import timezone
from apiclient import APIClient, HeaderAuthentication, JsonResponseHandler
from captcha.fields import ReCaptchaField
from django.conf import settings

class MembraClient(APIClient):
    def __init__(self, *args, **kwargs):
        kwargs['authentication_method'] = HeaderAuthentication(
            token=settings.MEMBRA_API_TOKEN,
            parameter="X-Membra-Api-Key",
            scheme=None,
            )
        kwargs['response_handler'] = JsonResponseHandler
        super().__init__(*args, **kwargs)
        
    def add_member(self, data):
        url = "https://api.membra.fi/public/v1/member"
        mdata = {
            'member_firstname': data['first_name'],
            'member_lastname': data['last_name'],
            'member_email': data['email'],
            'member_status': 'APPLICANT',
            'member_birthdate': '0001-01-01',
            'member_street': '-',
            'member_zipcode': 0,
            'member_city': '-',
            'member_sex': 'M',
            'member_accept_email_invoice': True,
            'member_entry_date': timezone.now().strftime('%Y-%m-%d')
        }
        result = self.post(url, data=mdata)
        if result['result_data']:
            result = self.get(url + '/' + str(result['result_data']))
        return result['result_data'][0]

class JoinOrganizationForm(forms.Form):
    first_name = forms.CharField(max_length=255, label='Etunimi')
    last_name = forms.CharField(max_length=255, label='Sukunimi')
    email = forms.EmailField(label='Sähköpostiosoite')
    
    captcha = ReCaptchaField()
    
    def save(self):
        c = MembraClient()
        member = c.add_member(self.cleaned_data)
        member['id'] = member['membership_id']
        member['name'] = member['member_firstname'] + ' ' + member['member_lastname']
        member['email'] = member['member_email']
        return member