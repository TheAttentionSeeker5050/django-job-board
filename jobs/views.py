from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from .models import Job

# Create your views here.

# list all jobs view
class AllJobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'jobs'
    
    def get_queryset(self):
        return Job.objects.all()