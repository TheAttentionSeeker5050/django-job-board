from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Resume, JobApplicant, Experience, Education
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from ..forms import ResumeForm, ExperienceForm, EducationForm, JobApplicantForm, ExperienceFormSet, EducationFormSet
from django.views.generic.edit import UpdateView
from django.urls import reverse


# create views to add the experience to the job applicant profile
class AddExperienceView(View, LoginRequiredMixin):
    # to add more experience or modify existing, we will use the PRG pattern, 
    # this will work for update, and delete as well
    # and will be reloaded into the same page, or probably just rehidrate the data
    def get(self, request, resume_pk):
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

        # find other experiences associated with this job applicant
        experiences = job_applicant.experience.all()

        # verify that user is the owner of the job applicant profile
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_experience', resume_pk=resume_pk)

        # add the form to the context
        context = {
            'form': ExperienceForm(),
            'job_applicant': job_applicant,
            'experiences': experiences,
        }
        
        return render(request, 'my_resume_add_work_experience.html', context)
    
    def post(self, request, resume_pk):
        # use the pk from the url to find the JobApplicant object
        job_applicant = JobApplicant.objects.get(pk=resume_pk)

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
            return redirect('my_resumes_add_experience', resume_pk=resume_pk)
        
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
            return redirect('my_resumes_add_experience', resume_pk=resume_pk)
        
        # if user owner not the same as the current user, unauthorized, 
        # for now it only will redirect to the same page
        if job_applicant.user_owner != request.user:
            return redirect('my_resumes_add_experience', resume_pk=resume_pk)

        # delete the experience
        experience.delete()

        # reload the page
        return redirect('my_resumes_add_experience', resume_pk=resume_pk)
    
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