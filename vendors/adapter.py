
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .views import account_activation_token

class MyAccountAdapter(DefaultAccountAdapter):

    def get_email_confirmation_redirect_url(self, request):
        data= request.user
        path = "/activate/{uid}/{token}/"
        return path.format(uid= urlsafe_base64_encode(force_bytes(data.pk)),token=account_activation_token.make_token(data))
