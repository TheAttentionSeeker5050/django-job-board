from django.db import models

# import the User model
from django.contrib.auth.models import User

# Create your models here.

class CompanyAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    