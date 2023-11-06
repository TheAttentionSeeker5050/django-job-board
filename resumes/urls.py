from django.urls import path
from .views import MyApplicantProfilesListView, JobApplicantCreateView, JobApplicantUpdateView, JobApplicantDeleteView, AddExperienceView, DeleteExperienceView, EditExperienceView,  AddEducationView, DeleteEducationView, EditEducationView

from .resume_detail_view import ResumeDetailView

# add the routes for the views here

urlpatterns = [
    path('', MyApplicantProfilesListView.as_view(), name='my_resumes_list'),
    path('create/', JobApplicantCreateView.as_view(), name='my_resumes_create'),
    path('create/<int:pk>/edit/', JobApplicantUpdateView.as_view(), name='my_resumes_edit'),
    path('create/<int:pk>/delete/', JobApplicantDeleteView.as_view(), name='my_resumes_delete'),
    
    # resume detail
    path('detail/<int:pk>/', ResumeDetailView.as_view(), name='my_resumes_detail'),

    # add the routes for the experience views
    path('create/<int:resume_pk>/add-experience/', AddExperienceView.as_view(), name='my_resumes_add_experience'),
    path('create/<int:resume_pk>/add-experience/<int:experience_pk>/delete/', DeleteExperienceView.as_view(), name='my_resumes_delete_experience'),
    path('create/<int:resume_pk>/add-experience/<int:experience_pk>/edit/', EditExperienceView.as_view(), name='my_resumes_edit_experience'),

    path('create/<int:resume_pk>/add-education/', AddEducationView.as_view(), name='my_resumes_add_education'),
    # path('create/<int:resume_pk>/add-education/', EducationCreateView.as_view(), name='my_resumes_add_education'),
    path('create/<int:resume_pk>/add-education/<int:education_pk>/delete/', DeleteEducationView.as_view(), name='my_resumes_delete_education'),
    path('create/<int:resume_pk>/add-education/<int:education_pk>/edit/', EditEducationView.as_view(), name='my_resumes_edit_education'),
]