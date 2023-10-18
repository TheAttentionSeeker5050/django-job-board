from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Resume, JobApplicant
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views import View
from .forms import ResumeForm, ExperienceForm, EducationForm, JobApplicantForm, ExperienceFormSet, EducationFormSet


# Create your views here.

# get all my owned job applicant profiles
class MyApplicantProfilesListView(LoginRequiredMixin, ListView):
    model = JobApplicant
    template_name = 'my_resumes_list.html'
    context_object_name = 'job_applicant'

    def get_queryset(self):
        return JobApplicant.objects.filter(user_owner=self.request.user)
    

# # create a new job applicant profile view
# class JobApplicantCreateView(LoginRequiredMixin, CreateView):
#     model = JobApplicant
#     template_name = 'my_resumes_create.html'
#     fields = ['title', 'resume_file', 'resume', 'education', 'experience']
#     success_url = reverse_lazy('my_resumes_list')

#     def form_valid(self, form):
#         form.instance.user_owner = self.request.user
#         return super().form_valid(form)


class JobApplicantCreateView(CreateView):
    model = JobApplicant
    form_class = JobApplicantForm
    template_name = 'my_resumes_create.html'
    success_url = reverse_lazy('success_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_form'] = ResumeForm()
        context['experience_formset'] = ExperienceFormSet()
        context['education_formset'] = EducationFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        resume_form = context['resume_form']
        experience_formset = context['experience_formset']
        education_formset = context['education_formset']

        if resume_form.is_valid() and experience_formset.is_valid() and education_formset.is_valid():
            print("done")

        return super().form_valid(form)