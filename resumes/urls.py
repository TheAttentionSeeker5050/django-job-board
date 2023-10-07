from django.urls import path
from .views import MyApplicantProfilesListView

# add the routes for the views here

urlpatterns = [
    path('', MyApplicantProfilesListView.as_view(), name='my_resumes_list'),
]