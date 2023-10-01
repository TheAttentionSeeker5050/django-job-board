from django.urls import path
from .views import ProfileView

# add the routes for the views here

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
]