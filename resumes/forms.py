from django import forms
from .models import JobApplicant, Resume, Education, Experience
from django.forms import formset_factory

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['term', 'title', 'company']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['term', 'title', 'institution']

ExperienceFormSet = formset_factory(ExperienceForm, extra=1)
EducationFormSet = formset_factory(EducationForm, extra=1)

class JobApplicantForm(forms.ModelForm):
    skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'skill-input'}), required=False)

    # allow to create a new resume, experience, and education on job applicant creation
    resume = ResumeForm()
    
    class Meta:
        model = JobApplicant
        # fields = ['title', 'resume_file', 'skills']
        fields = ['title', 'resume_file', 'skills']
