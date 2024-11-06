
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    country = models.CharField(max_length= 255,blank=True)
    phone_number = models.CharField(max_length=10,blank=True)

    def __str__(self) -> str:
        return self.username