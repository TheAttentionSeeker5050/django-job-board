from django.db import models
from users.models import CustomUser

class Resume(models.Model):
    file_path = models.FileField(upload_to='resumes/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # return string
    def __str__(self):
        return self.user + " - " + self.file_path.name