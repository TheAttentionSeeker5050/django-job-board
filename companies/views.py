from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company

# Create your views here, all of the views will be class based views

# display all companies owned by the user
# will find all the companies that the user has link with in CompanyAdmin model
class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    

    def get_queryset(self):
        return Company.objects.filter(companyadmin__user=self.request.user)