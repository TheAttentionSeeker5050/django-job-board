from django.urls import path
from .views import AllJobListView, JobCreateView, JobUpdateView, JobDeleteView, JobDetailView

urlpatterns = [
    # list jobs view
    path('', AllJobListView.as_view(), name='list_jobs'),

    # job detail view
    path('<int:id>/', JobDetailView.as_view(), name='job_detail'),

    # update job view
    path('update/<int:pk>/', JobUpdateView.as_view(), name='update_job'),

    # delete job view
    path('delete/<int:id>/', JobDeleteView.as_view(), name='delete_job'),
]