from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Resume, JobApplicant


# Create your views here.

# get all my owned job applicant profiles
class MyApplicantProfilesListView(LoginRequiredMixin, ListView):
    model = JobApplicant
    template_name = 'my_resumes_list.html'
    context_object_name = 'job_applicant'

    def get_queryset(self):
        return JobApplicant.objects.filter(user_owner=self.request.user)