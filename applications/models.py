from django.db import models
from users.models import CustomUser
from jobs.models import Job
from resumes.models import Resume
from companies.models import Company

class Application(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    questions_and_answers = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    # return string
    def __str__(self):
        return self.user + " - " + self.job