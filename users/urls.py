from django.urls import path
from .views import ProfileView, ProfileUpdateView, ProfileDeleteView

# add the routes for the views here

urlpatterns = [
    # get profile by session id
    path('', ProfileView.as_view(), name='profile'),
    # edit profile
    path('edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    # delete profile
    path('delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]