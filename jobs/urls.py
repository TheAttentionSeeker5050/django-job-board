from django.urls import path
from .views import AllJobListView

urlpatterns = [
    # list jobs view
    path('', AllJobListView.as_view(), name='list-jobs'),
]