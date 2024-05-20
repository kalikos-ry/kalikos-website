from apiclient import APIClient, HeaderAuthentication, JsonResponseHandler
from django.utils import timezone
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

    def find_member(self, email):
        url = "https://api.membra.fi/v2/member/filter/"
        result = self.get(url, params={'filter[filters][0][field]': 'mem_email', 'filter[filters][0][value]': email, 'filter[filters][0][operator]': 'eq'})
        if (result['http_status'] == 200):
            return result['data'][0] if len(result['data']) > 0 else None
        return None
