#     vendors
from django.urls import path
from . import views
    
urlpatterns = [
    path("vendor/signup/",views.vendor_signup,name="vendor-signup"),
    path("vendor/dashboard/",views.vendor_dashboard,name="vendor-dashboard"),
    path("vendor/login/",views.vendor_login,name="vendor-login"),
    path('activate/<slug:uidb64>/<slug:token>/',  
        views.activate, name='activate'), 
]

    
    