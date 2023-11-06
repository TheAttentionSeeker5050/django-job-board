from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Resume, JobApplicant, Experience, Education
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from .forms import ResumeForm, ExperienceForm, EducationForm, JobApplicantForm, ExperienceFormSet, EducationFormSet
from django.views.generic.edit import UpdateView


# Create your views here.

# get all my owned job applicant profiles
class MyApplicantProfilesListView(LoginRequiredMixin, ListView):
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
            # save the form
            self.object = form.save()
            # add the model object pk and redirect to the add experience view
            return redirect('my_resumes_add_experience', pk=self.object.pk)

        return super().form_valid(form)
    
class JobApplicantUpdateView(UpdateView, LoginRequiredMixin):
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
            # save the form
            self.object = form.save()
            # add the model object pk and redirect to the add experience view
            return redirect('my_resumes_add_experience', pk=self.object.pk)

        return super().form_valid(form)

class JobApplicantDeleteView(View, LoginRequiredMixin):
    def post(self, request, pk):
        # find the job applicant
        job_applicant = JobApplicant.objects.get(pk=pk)
        # verify that the user is the owner of the job applicant
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_list')
        # delete the job applicant
        job_applicant.delete()
        # redirect to the job applicant list
        return redirect('my_resumes_list')

    
    
# create views to add the experience to the job applicant profile
class AddExperienceView(View, LoginRequiredMixin):
    # to add more experience or modify existing, we will use the PRG pattern, 
    # this will work for update, and delete as well
    # and will be reloaded into the same page, or probably just rehidrate the data
    def get(self, request, experience_pk):
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=experience_pk)

        # find other experiences associated with this job applicant
        experiences = job_applicant.experience.all()

        # verify that user is the owner of the job applicant profile
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_experience', pk=experience_pk)

        # add the form to the context
        context = {
            'form': ExperienceForm(),
            'job_applicant': job_applicant,
            'experiences': experiences,
        }
        
        return render(request, 'my_resume_add_work_experience.html', context)
    
    def post(self, request, experience_pk):
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=experience_pk)

        # find other experiences associated with this job applicant
        experiences = job_applicant.experience.all()

        # add the form to the context
        context = {
            'form': ExperienceForm(),
            'job_applicant': job_applicant,
            'experiences': experiences,
        }

        # create the form from the post data
        form = ExperienceForm(request.POST)

        # validate the form
        if form.is_valid():
            # save the form
            experience = form.save()
            # add the experience to the job applicant
            job_applicant.experience.add(experience)
            # reload the page
            return redirect('my_resumes_add_experience', pk=experience_pk)
        
        return render(request, 'my_resume_add_work_experience.html', context)

    
# the following is a class based view to edit or delete an experience
class DeleteExperienceView(View, LoginRequiredMixin):
    
    def post(self, request, resume_pk, experience_pk):
        """ delete the experience """
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find the experience="edit-education" class="bg-emerald-500  to delete
        experience = Experience.objects.get(pk=experience_pk)

        # find other experiences associated with this job applicant
        experiences = job_applicant.experience.all()

        # verify that the job experience has foreign key experience, if not return bad request
        if experience not in job_applicant.experience.all():
            return redirect('my_resumes_add_experience', pk=resume_pk)
        
        # if user owner not the same as the current user, unauthorized, 
        # for now it only will redirect to the same page
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_experience', pk=resume_pk)

        # delete the experience
        experience.delete()

        # reload the page
        return redirect('my_resumes_add_experience', pk=resume_pk)
    
class EditExperienceView(View, LoginRequiredMixin):
    # get the view template for edit
    def get(self, request, resume_pk, experience_pk):
        """ get the edit template """
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find the experience to delete
        current_work_experience = Experience.objects.get(pk=experience_pk)

        # find other experiences associated with this job applicant
        experiences = job_applicant.experience.all()

        # verify that the job experience has foreign key experience, if not return bad request
        if current_work_experience not in job_applicant.experience.all():
            return redirect('my_resumes_add_experience', pk=resume_pk)
        
        # if user owner not the same as the current user, unauthorized, 
        # for now it only will redirect to the same page
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_experience', pk=resume_pk)

        # add the form to the context
        context = {
            'form': ExperienceForm(
                initial={
                    'term': current_work_experience.term,
                    'title': current_work_experience.title,
                    'company': current_work_experience.company,
                }
            ),
            'job_applicant': job_applicant,
            'experiences': experiences,
            'edit_form': True,
        }

        return render(request, 'my_resume_add_work_experience.html', context)
    
    # edit the view
    def post(self, request, resume_pk, experience_pk):
        """ edit the experience """
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find the experience to edit
        experience = Experience.objects.get(pk=experience_pk)

        # verify that the job experience has foreign key experience, if not return bad request
        if experience not in job_applicant.experience.all():
            return redirect('my_resumes_add_experience', pk=resume_pk)
        
        # if user owner not the same as the current user, unauthorized, 
        # for now it only will redirect to the same page
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_experience', pk=resume_pk)

        # edit the experience
        experience.term = request.POST['term']
        experience.title = request.POST['title']
        experience.company = request.POST['company']

        # save the experience
        experience.save()

        # reload the page
        return redirect('my_resumes_add_experience', pk=resume_pk)
    

# education templates
class AddEducationView(View, LoginRequiredMixin):
    def get(self, request, resume_pk):
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find other experiences associated with this job applicant
        educations = job_applicant.education.all()

        # verify that user is the owner of the job applicant profile
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_education', resume_pk=resume_pk)

        # add the form to the context
        context = {
            'form': EducationForm(),
            'job_applicant': job_applicant,
            'educations': educations,
        }
        
        return render(request, 'my_resume_add_education.html', context)
    
    def post(self, request, resume_pk):
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find other experiences associated with this job applicant
        educations = job_applicant.education.all()

        # add the form to the context
        context = {
            'form': EducationForm(),
            'job_applicant': job_applicant,
            'educations': educations,
        }

        # create the form from the post data
        form = EducationForm(request.POST)

        # validate the form
        if form.is_valid():
            # save the form
            education = form.save()
            # add the experience to the job applicant
            job_applicant.education.add(education)
            # reload the page
            return redirect('my_resumes_add_education', resume_pk=resume_pk)
        
        # re-render site
        return render(request, 'my_resume_add_education.html', context)

# the following is a class based view to delete an education
class DeleteEducationView(View, LoginRequiredMixin):
        
    
    def post(self, request, resume_pk, education_pk):
        """ delete the education """
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find the education to delete
        education = Education.objects.get(pk=education_pk)

        # find other educations associated with this job applicant
        educations = job_applicant.education.all()

        # verify that the job education has foreign key education, if not return bad request
        if education not in job_applicant.education.all():
            return redirect('my_resumes_add_education', resume_pk=resume_pk)
        
        # if user owner not the same as the current user, unauthorized, 
        # for now it only will redirect to the same page
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_education', resume_pk=resume_pk)

        # delete the education
        education.delete()

        # reload the page
        return redirect('my_resumes_add_education', resume_pk=resume_pk)

class EditEducationView(View, LoginRequiredMixin):
    # get the view template for edit
    def get(self, request, resume_pk, education_pk):
        """ get the edit template """
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find the education to delete
        current_education = Education.objects.get(pk=education_pk)

        # find other educations associated with this job applicant
        educations = job_applicant.education.all()

        # verify that the job education has foreign key education, if not return bad request
        if current_education not in job_applicant.education.all():
            return redirect('my_resumes_add_education', resume_pk=resume_pk)
        
        # if user owner not the same as the current user, unauthorized, 
        # for now it only will redirect to the same page
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_education', resume_pk=resume_pk)

        # add the form to the context
        context = {
            'form': EducationForm(
                initial={
                    'term': current_education.term,
                    'title': current_education.title,
                    'institution': current_education.institution,
                }
            ),
            'job_applicant': job_applicant,
            'educations': educations,
            'edit_form': True,
        }

        return render(request, 'my_resume_add_education.html', context)
    
    # edit the view
    def post(self, request, resume_pk, education_pk):
        """ edit the education """
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find the education to edit
        education = Education.objects.get(pk=education_pk)

        # verify that the job education has foreign key education, if not return bad request
        if education not in job_applicant.education.all():
            return redirect('my_resumes_add_education', resume_pk=resume_pk)
        
        # if user owner not the same as the current user, unauthorized, 
        # for now it only will redirect to the same page
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_education', resume_pk=resume_pk)
        
        # edit the education
        education.term = request.POST['term']
        education.title = request.POST['title']
        education.institution = request.POST['institution']

        # save the education
        education.save()

        # reload the page
        return redirect('my_resumes_add_education', resume_pk=resume_pk)
    
