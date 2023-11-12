from django.urls import path
from .views import DirectApplyCreateView, ApplicationsListView

urlpatterns = [
    path('direct-apply/<int:job_pk>/', DirectApplyCreateView.as_view(), name='direct_apply'),
    path('list-by-job/<int:job_pk>/', ApplicationsListView.as_view(), name='applications_list'),
    path('detail/<int:application_pk>', ApplicationsListView.as_view(), name='applications_detail'),
    path('delete/<int:application_pk>/', ApplicationsListView.as_view(), name='applications_delete'),

]