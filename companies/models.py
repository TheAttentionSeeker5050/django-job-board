from django.db import models
from users.models import CustomUser

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.company_name