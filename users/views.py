# # implement login using class based views using session authentication
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import ListView, CreateView
# from django.contrib.auth import get_user_model
# from django.urls import reverse_lazy
# from django.contrib.auth.views import LoginView, LogoutView, CreateView
# from .forms import UserCreateForm, UserLoginForm

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegisterForm

# Create your views here.
# create the login view using classes and forms

class UserLoginView(LoginView):
    template_name = 'login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

# class UserLoginView(LoginView):
#     """A view that logs a user in, with no privileges, from the given username and password."""
#     template_name = 'login.html'
#     form_class = UserLoginForm
#     success_url = reverse_lazy('home')
#     redirect_authenticated_user = True

# # create the create account view using classes and forms
# class UserCreateView(CreateView):
#     """A view that creates a user, with no privileges, from the given username and password."""
#     template_name = 'register.html'
#     form_class = UserCreateForm
#     success_url = reverse_lazy('login')
#     redirect_authenticated_user = True

# # create the logout view using classes
# class UserLogoutView(LoginRequiredMixin, ListView):
#     """A view that logs a user out, with no privileges, from the given username and password."""
#     template_name = 'logout.html'
#     redirect_authenticated_user = True
#     success_url = reverse_lazy('home')

    
#     def get_queryset(self):
#         # get the current user
#         return get_user_model().objects.all()
    