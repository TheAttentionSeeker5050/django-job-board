from django.db import models

# Create your models here.
from companies.models import Company
from tinymce import models as tinymce_models

# job model
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = tinymce_models.HTMLField(default='', blank=True, null=True)
    location = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    external_link = models.URLField(blank=True, null=True)
    
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
    qualifications = tinymce_models.HTMLField(default='')
    responsibilities = tinymce_models.HTMLField(default='')
    skills_required = tinymce_models.HTMLField(default='')
    deadline = models.DateField(blank=True, null=True)


    # return string
    def __str__(self):
        return self.title