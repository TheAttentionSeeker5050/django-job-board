from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company
from .forms import CompanyCreateForm
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from jobs.models import Job

# forbidden django response
from django.http import HttpResponseForbidden, HttpResponseRedirect


# Create your views here, all of the views will be class based views

# display all companies owned by the user
# will find all the companies that the user has link with in CompanyAdmin model
class MyOrganizationsCompanyListView(LoginRequiredMixin, ListView):
    """Display a list of companies that the user owns"""
    model = Company
    template_name = 'company_my_organizations.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)
    
# display all companies
class AllCompanyListView(ListView):
    """Display a list all companies"""
    model = Company
    template_name = 'company_list.html'
    context_object_name = 'companies'
    
    def get_queryset(self):
        return Company.objects.all()
    
class CreateCompanyView(LoginRequiredMixin, CreateView):
    """Create a new company page"""
    model = Company
    template_name = 'company_create.html'
    form_class = CompanyCreateForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my_organizations')

    def form_invalid(self, form):
        return redirect('home')
    

# display edit organization page
class EditCompanyView(LoginRequiredMixin, UpdateView):
    """Edit a company page"""
    model = Company
    template_name = 'company_update.html'
    form_class = CompanyCreateForm
    context_object_name = 'company'
    
    
    def get_success_url(self):
        return reverse('my_organizations')
    
    def form_invalid(self, form):
        return redirect('home')
    
    def form_valid(self, form):
        # verify that the request user is the owner
        if self.object.owner == self.request.user:
            form.save()
            return super().form_valid(form)
        else:
            return HttpResponseForbidden("You don't have permission to edit this company.")
        
    
# display delete organization page
class DeleteCompanyView(LoginRequiredMixin, DeleteView):
    """Delete a company page"""
    model = Company
    template_name = 'company_delete.html'
    context_object_name = 'company'
    success_url = reverse_lazy('my_organizations')  # Your success URL
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner == self.request.user:  # Check if the logged-in user is the owner
            self.object.delete()
            return redirect(self.get_success_url())
        else:
            return HttpResponseForbidden("You don't have permission to delete this company.")


class CompanyDetailView(DetailView):
    """Display a company page with all the jobs posted by the company"""
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.filter(company=self.object)
        context['is_owner'] = self.request.user == self.object.owner
        context['previous_url'] = self.request.META.get('HTTP_REFERER', '/')
        return context