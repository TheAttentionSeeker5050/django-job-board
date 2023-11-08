# pylint: disable=too-many-ancestors
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from resumes.models import JobApplicant
from django.views.generic.edit import CreateView
from django.views import View
from django.views.generic.edit import UpdateView
from django.urls import reverse


# get all my owned job applicant profiles
class MyApplicantProfilesListView(ListView, LoginRequiredMixin):
    """ Renders a list of all Job Applicant Profiles."""
    model = JobApplicant
    template_name = 'my_resumes_list.html'
    context_object_name = 'job_applicant'
    
    def get_queryset(self):
        # print(self.request.user)
        # print(JobApplicant.objects.filter(user_owner=self.request.user))
        return JobApplicant.objects.filter(user_owner=self.request.user)
        
    

# job applicant profiles consist of the following steps.
# 1. create a resume: job applicant profile
# 2. add experience to the job applicant profile, each in its own post form
# 3. add education to the job applicant profile, each in its own post form

class JobApplicantCreateView(CreateView, LoginRequiredMixin):
    """ Renders a form to create a new Job Applicant Profile."""
    model = JobApplicant
    fields = ['title', 'resume_file', 'skills']
    template_name = 'my_resumes_create3.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        # add user_owner to the form
        form.instance.user_owner = self.request.user
        context = self.get_context_data()
        

        if form.is_valid():

            # validate that resume file can only accept pdf files
            if form.cleaned_data['resume_file'].content_type != 'application/pdf':
                context['form'] = form
                # add errors to the context array
                context['errors'] = ['Resume file must be a pdf file']
                return render(self.request, 'my_resumes_create3.html', context)
            
            
            # save the form
            self.object = form.save()
            # add the model object pk and redirect to the add experience view
            return redirect('my_resumes_add_experience', resume_pk=self.object.pk)

        return super().form_valid(form)
    
class JobApplicantUpdateView(UpdateView, LoginRequiredMixin):
    """ Renders a form to update a Job Applicant Profile."""
    model = JobApplicant
    fields = ['title', 'resume_file', 'skills']
    template_name = 'my_resumes_create3.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['job_applicant'] = JobApplicant.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        # add user_owner to the form
        form.instance.user_owner = self.request.user
        context = self.get_context_data()
        

        if form.is_valid():

            # because we are uploading a form, them we have to do a try catch
            try:
                # verify if there is a new resume_file in the form
                if form.cleaned_data['resume_file'].content_type != 'application/pdf':
                    context['form'] = form
                    # add errors to the context array
                    context['errors'] = ['Resume file must be a pdf file']
                    return render(self.request, 'my_resumes_create3.html', context)
            except AttributeError:
                # do nothing, because the user did not upload a new resume file
                pass
            # save the form
            self.object = form.save()
            # add the model object pk and redirect to the add experience view
            return redirect('my_resumes_add_experience', resume_pk=self.object.pk)

        return super().form_valid(form)

class JobApplicantDeleteView(View, LoginRequiredMixin):
    """ Renders a form to delete a Job Applicant Profile."""
    def post(self, request, pk):
        # find the job applicant
        job_applicant = JobApplicant.objects.get(pk=pk)
        # verify that the user is the owner of the job applicant
        if job_applicant.user_owner != request.user:
            # add error 
            return redirect(reverse('my_resumes_list'), kwargs={'errors': ['You are not authorized to delete this job applicant profile']})
        

        # delete the job applicant
        job_applicant.delete()
        # redirect to the job applicant list
        return redirect('my_resumes_list')

    