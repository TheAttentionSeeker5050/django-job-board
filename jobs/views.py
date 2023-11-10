from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from .models import Job
from .forms import JobCreateForm
from companies.models import Company
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

# list all jobs view
class AllJobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'jobs'
    
    def get_queryset(self):
        return Job.objects.all()
    
# list jobs by company detail view
class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        # filter by url param id=job.id
        return Job.objects.filter(id=self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = Job.objects.get(id=self.kwargs.get('pk'))
        context['is_owner'] = self.request.user == self.get_object().company.owner
        context['previous_url'] = self.request.META.get('HTTP_REFERER', '/')
        return context

# create job view
class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    template_name = 'job_create.html'
    form_class = JobCreateForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        # add the company on the url to the form
        form.instance.company = Company.objects.get(id=self.kwargs['company_pk'])
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    
    # get success url
    def get_success_url(self):
        return reverse_lazy('company_detail', kwargs={'pk': self.kwargs['company_pk']})
    
# update job view
class JobUpdateView(LoginRequiredMixin, UpdateView):
    model = Job
    template_name = 'job_update.html'
    form_class = JobCreateForm
    context_object_name = 'job'
    
    
    def form_valid(self, form):
        # verify that the request user is the owner
        if self.object.company.owner == self.request.user:
            form.save()
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("You don't have permission to edit this job.")
        
    # if any field is invalid in the form, render error on template
    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(JobUpdateView, self).get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs.get('pk'))
        return context
    
    def get_success_url(self):
        # get the pk of the Company this job belongs to
        company_pk = Job.objects.get(id=self.kwargs['pk']).company.id
        return reverse_lazy('company_detail', kwargs={'pk': company_pk})


# delete job view
class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    template_name = 'job_delete.html'
    success_url = reverse_lazy('my_organizations')
    context_object_name = 'job'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.company.owner == self.request.user: # Check if the logged-in user is the owner
            self.object.delete()
            return redirect(self.get_success_url())
        else:
            return HttpResponseForbidden("You don't have permission to delete this job.")
    
    def get_queryset(self):
        # filter by url param id=job.id
        return Job.objects.filter(id=self.kwargs['pk'])