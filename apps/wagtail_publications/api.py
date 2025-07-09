from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import path, include
from apps.home.models import SnipcartSettings
from apps.organization.membra import MembraClient
import requests

class CheckDiscount(APIView):
  @classmethod
  def get_urlpatterns(cls):
      """
      This returns a list of URL patterns for the endpoint
      """
      return [
          path("", cls.as_view(), name="discount_code"),
      ]

  def get(self, request):
    api_key = SnipcartSettings.load(request_or_site=request).secret_api_key
    member_discount_name = SnipcartSettings.load(request_or_site=request).member_discount_name
    email = request.GET["email"]
    if api_key:
        client = MembraClient()
        member = client.find_member(email)
        if member is None or member['mes_status'] != "1":
            return Response({"email": email, "status": member["mes_status"] if member else "not found"})
        headers = { 'Accept' : 'application/json' }
        discounts = requests.get('https://app.snipcart.com/api/discounts', params=(('limit', 100),), auth=(api_key,''), headers=headers)
        if discounts.status_code == 200:
          for d in discounts.json():
              if d['name'] == member_discount_name:
                  return Response({"discount": { "id": d["id"], "name": d["name"], "code": d["code"] }, "email": email})
        return Response({"email": email, "status": "no discount with name " + member_discount_name})
    return Response({"email": email, "status": "no api key"})