from django.db import models
from users.models import CustomUser
from django.contrib.postgres.fields import ArrayField

class Resume(models.Model):
    
    title = models.CharField(max_length=100, verbose_name='Title')
    user_owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        default=0,
    )

    def __str__(self):
        return f"{self.title}"
    


class Experience(models.Model):
    term = models.CharField(max_length=50, verbose_name='Term')
    title = models.CharField(max_length=100, verbose_name='Job Title')
    company = models.CharField(max_length=100, verbose_name='Institution')

    def __str__(self):
        return f"{self.title} at {self.company}"
    
class Education(models.Model):
    term = models.CharField(max_length=50, verbose_name='Term')
    title = models.CharField(max_length=100, verbose_name='Job Title')
    institution = models.CharField(max_length=100, verbose_name='Institution')


    def __str__(self):
        return f"{self.title} at {self.institution}"

class JobApplicant(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    resume_file = models.FileField(upload_to='resumes/uploads/', verbose_name='Resume File')

    user_owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        default=0,
        related_name='job_applicant_profile'
    )

    education = models.ManyToManyField(
        Education,
        verbose_name='Education',
        blank=True
    )

    experience = models.ManyToManyField(
        Experience,
        verbose_name='Work Experience',
        blank=True
    )
    
    skills = ArrayField(
        models.CharField(max_length=50, blank=True),
        verbose_name='Skills',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} "

    class Meta:
        verbose_name = 'Job Applicant'
        verbose_name_plural = 'Job Applicants'