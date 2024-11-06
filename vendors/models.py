import django
from django.db import models
from adminapp.models import User
# from django.contrib.auth.models import User 
# Create your models here.
class Vendors(models.Model):
    vendor = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    shop_name = models.CharField(max_length= 255,default="daraznepal")
    shop_number = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    phone_number = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_now_add =True)
    pan_vat = models.IntegerField(default=0)


    def __str__(self) -> str:
        return self.vendor.username