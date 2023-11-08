# imports here
from django.shortcuts import render
from django.views import View

# here goes the custom views
class ResumeDetailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'my_resume_detail.html', {})