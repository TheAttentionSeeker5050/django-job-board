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
from .forms import RegisterForm, UserLoginForm
from django.views.generic import DetailView
from django.contrib.auth import get_user_model

# Create your views here.
# create the login view using classes and forms

class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  
    success_url = reverse_lazy('home')
    form_class = UserLoginForm

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

# create a profile view
class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_object'

    # find user by auth id
    def get_object(self):
        return get_user_model().objects.get(id=self.request.user.id)