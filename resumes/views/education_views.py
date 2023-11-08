from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from resumes.models import JobApplicant, Education
from django.views import View
from resumes.forms import EducationForm



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
    


