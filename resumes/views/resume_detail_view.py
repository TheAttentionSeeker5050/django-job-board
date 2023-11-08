# imports here
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from resumes.models import JobApplicant
from users.models import CustomUser

# # here goes the custom views
# class ResumeDetailView(View):
#     def get(self, request, resume_pk):
#         return render(request, 'my_resume_detail.html', {})

class ResumeDetailView(DetailView):
    """ Renders a specific Job Applicant Profile based on it's pk."""
    model = JobApplicant
    template_name = 'my_resume_detail.html'
    context_object_name = 'job_applicant'
    
    # I have an url param called resume_pk, so I need to override the get_object method
    def get_object(self):
        return JobApplicant.objects.get(pk=self.kwargs['resume_pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_applicant_data'] = JobApplicant.objects.get(pk=self.kwargs['resume_pk'])

        print("job applicant data: ", context['job_applicant_data'])

        # add the user data to the context, search in the database the user first, last name and email search user by user_owner
        userObj = CustomUser.objects.get(pk=context['job_applicant_data'].user_owner.pk)

        # find all the education and experience with applicant id as resume_pk
        educationObj = context['job_applicant_data'].education.all()
        experienceObj = context['job_applicant_data'].experience.all()

        # add the education and experience to the context
        context['education'] = educationObj
        context['experience'] = experienceObj
        

        userDataObj = {
            'first_name': userObj.first_name,
            'last_name': userObj.last_name,
            'email': userObj.email
        }

        context['user_data'] = userDataObj

        

        # if is the owner of the resume, then add the context
        if context['job_applicant_data'].user_owner == self.request.user:
            context['is_owner'] = True
        else:
            context['is_owner'] = False
        return context
    
    
    
    