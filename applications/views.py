from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from .models import Application
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from jobs.models import Job
from companies.models import Company
from resumes.models import JobApplicant
from django.shortcuts import redirect
from website.permissions import isOwnerOfObject



# Create your views here.
# create class Views
class DirectApplyCreateView(LoginRequiredMixin, CreateView):
    model = Application
    template_name = 'direct_apply.html'
    fields = ['job', 'job_applicant_profile', 'company']
    context_object_name = 'application'
    login_url = "/login/"

    # now get the context data with method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # first get job from url params
        context["job"] = Job.objects.get(id=self.kwargs.get('job_pk'))
        # find the company that holds the job offer and add it to the context
        context["company"] = Company.objects.get(id=context["job"].company.id)
        # get the job applicant profiles owned by request user
        context["job_applicant_profiles"] = JobApplicant.objects.filter(user_owner=self.request.user)
        return context
    
    # on form valid
    def form_valid(self, form):
        
        # choose the selected object id of the job applicant profile html select job_applicant_profile
        form.instance.job_applicant_profile = JobApplicant.objects.get(id=form.instance.job_applicant_profile.id)
        
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        # add errors to context
        context = self.get_context_data()

        return render(self.request, "direct_apply.html", context=context)
    
    # add success redirect url
    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.kwargs['job_pk']})
    
class ApplicationsListView(UserPassesTestMixin, ListView):
    model = Application
    template_name = 'applications_list.html'
    context_object_name = 'job_applications'
    # if not logged in, redirect to login page
    login_url = '/login/'
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # return all the applications that belong to the job
        context = super().get_context_data(**kwargs)
        # user must be the owner of the job, otherwise redirect to home
        context['job_applications'] = Application.objects.filter(job=self.kwargs['job_pk'])
        return context
    
    def test_func(self):
        # get the job
        job = Job.objects.get(id=self.kwargs['job_pk'])
        # we call our custom permission test function
        return isOwnerOfObject(self, job.company.owner)
        

class ApplicationDetailView(UserPassesTestMixin, DetailView):
    model = Application
    template_name = 'applications_detail.html'
    slug_field = 'pk'
    slug_url_kwarg = 'application_pk'
    context_object_name = 'application'
    # if not logged in, redirect to main page
    login_url = '/'

    def get_queryset(self):
        # get application
        queryset = super().get_queryset()
        # get the application with the kwargs
        return queryset.filter(id=self.kwargs['application_pk'])
    
    def test_func(self):
        # get the queryset application
        application = self.get_queryset().first()

        # get the company owner for this application
        company_owner = application.company.owner

        # use custom permission test function
        return isOwnerOfObject(self, company_owner)