from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    industry = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    # return string
    def __str__(self):
        return self.company_name