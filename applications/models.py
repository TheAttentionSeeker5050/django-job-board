from django.db import models
from jobs.models import Job
from resumes.models import JobApplicant
from companies.models import Company

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=0)
    job_applicant_profile = models.ForeignKey(JobApplicant, default=0, on_delete=models.CASCADE)
    questions_and_answers = models.TextField() # we will not use this for the moment
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # return string
    def __str__(self):
        # should return first name, last name and job title
        return "something"
        # return f"{self.job_applicant_profile__user_owner__first_name} {self.job_applicant_profile__user_owner__last_name} - {self.job__title}"