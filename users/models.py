from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

# Create your models here.



class CustomUser(AbstractUser):
    # add additional fields in here
    email = models.EmailField(unique=True)
    # return self.email
    def __str__(self):
        return self.email
    

# class CompanyAdmin(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
#     is_admin = models.BooleanField(default=True)

#     def __str__(self):
        return self.user + "@" + self.company


    