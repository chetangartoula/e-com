from django.template.loader import render_to_string  
from django.shortcuts import  HttpResponse, render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login
from .forms import VendorLoginForm, vendorCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_str
import six
# Create your views here.
def vendor_dashboard(request):
    return render(request,"vendors/vendor_dashboard.html")

def vendor_signup(request):
    current_site = get_current_site(request)
    print(current_site)

    form = vendorCreationForm
    if request.method =="POST":
        form = vendorCreationForm(request.POST)
        if form.is_valid():
            data = form.save(request)

            # print(form(request))
            # form.save(request)
            user = form.cleaned_data.get("first_name")

            email = form.cleaned_data.get("email")

            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message=  render_to_string('account/acc_active_email.html', {  
                'user': user,  
                'domain': "localhost:8000",  
                'uid':urlsafe_base64_encode(force_bytes(data.pk)),  
                'token':account_activation_token.make_token(data),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  


            # print(user)

            messages.success(request,f'{user} We are sending the message to your {email}')
            return redirect("vendor-login")
    context={"form":form}
    return render(request,"vendors/verdor_registration.html",context)


def vendor_login(request):
    form = VendorLoginForm
    if request.method =="POST":
        form = VendorLoginForm(request=request, data=request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data.get("login")
                password = form.cleaned_data.get("password")
                print(username,password)
                user = authenticate(username=username,password=password)
                print(user)
                if user is not None:
                    login(request,user)
                    return redirect("admin-login")
                else:
                    messages.error(request,"You are not valid vendor !!!")
                    return redirect("vendor-login")
            else:
                messages.error(request,"Email or password did not match please try again !!!")
                return redirect("vendor-login")
        except:
            messages.error(request,"Email or password did not match please try again !!!")
            return redirect("vendor-login")

    context={"form":form}
    return render(request,"vendors/vendor_login.html",context)


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_vendor = True  
        user.save()  
        messages.success(request,"Thank you for your email confirmation. Now you can login your account.'")
        return redirect('vendor-login')  
    else:
        messages.error(request,"Sorry !!! You are not activate . Please Try again")
        return redirect("vendor-signup")  



 
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (  
                six.text_type(user.id) + six.text_type(timestamp) +  
                six.text_type(user.is_active)  
            )
account_activation_token = TokenGenerator()  