from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .models import Application
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from jobs.models import Job
from companies.models import Company
from resumes.models import JobApplicant



# Create your views here.
# create class Views
class DirectApplyCreateView(CreateView, LoginRequiredMixin):
    model = Application
    template_name = 'direct_apply.html'
    fields = ['job', 'job_applicant_profile', 'company']
    context_object_name = 'application'

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
    
class ApplicationsListView(ListView, LoginRequiredMixin):
    model = Application
    template_name = 'applications_list.html'
    context_object_name = 'job_applications'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # return all the applications that belong to the job
        context = super().get_context_data(**kwargs)
        context['job_applications'] = Application.objects.filter(job=self.kwargs['job_pk'])
        return context
    
    