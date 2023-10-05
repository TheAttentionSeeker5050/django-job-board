from django.db import models

# Create your models here.
from companies.models import Company

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    # Additional Fields
    employment_type = models.CharField(
        max_length=50,
        choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Contract', 'Contract')],
        default='Full-time'
    )
    experience_level = models.CharField(
        max_length=50,
        choices=[('Entry', 'Entry'), ('Mid', 'Mid'), ('Senior', 'Senior')],
        default='Entry'
    )
    salary_range = models.CharField(max_length=50, blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    skills_required = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)

    # return string
    def __str__(self):
        return self.title