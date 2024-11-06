
from django import forms
from django.db import transaction
from adminapp.models import User
from random_username.generate import generate_username
# from django.contrib.auth.models import User
from .models import  Vendors
from allauth.account.forms import SignupForm,LoginForm


class vendorCreationForm(SignupForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    shop_name = forms.CharField(max_length=255,required=True)
    shop_number = forms.CharField(max_length=255, required=True)
    location = forms.CharField(max_length=255, required=True)
    phone_number = forms.IntegerField( required=True)
    pan_vat = forms.IntegerField(required=True)
    # email = forms.EmailField(required=True)


    class Meta(SignupForm):
        model = User
        # fields= ["first_name","last_name","email"]
        
    @transaction.atomic
    def save(self,request):
        user = super(vendorCreationForm,self).save(request)
        user.is_vendor = False
        user.is_active = True
        user.phone_number = self.cleaned_data.get("phone_number")
        user.country = self.cleaned_data.get("location")
        user.username = f'{generate_username(1)[0]}'
        # user.first_name = self.cleaned_data.get("first_name")
        # user.last_name = self.cleaned_data.get("last_name")
        user.save()
        vendor = Vendors.objects.create(vendor=user)
        vendor.shop_number = self.cleaned_data.get("shop_number")
        vendor.shop_name = self.cleaned_data.get("shop_name")
        vendor.location = self.cleaned_data.get("location")
        # vendor.phone_number = self.cleaned_data.get("phone_number")
        vendor.pan_vat = self.cleaned_data.get("pan_vat")

        vendor.save()
        return user


class VendorLoginForm(LoginForm):

    def login(self, *args, **kwargs):
        print(args,kwargs)
        # Add your own processing here.

        # You must return the original result.
        return super(VendorLoginForm, self).login(*args, **kwargs)