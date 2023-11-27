# pylint: disable=super-with-arguments
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import RegisterForm, UserLoginForm
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

# Create your views here.
# create the login view using classes and forms

class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True  
    success_url = reverse_lazy('home')
    form_class = UserLoginForm

    # add a context to the form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    # if form is invalid redirect to same page but charge the context to error
    def form_invalid(self, form):
        context = self.get_context_data()
        context['form'] = form
        context['error_message'] = 'Invalid form'
        return self.render_to_response(context)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login') # redirect to login page after successful registration
    
    # add a context to the form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    # if form is invalid redirect to same page but charge the context to error
    def form_invalid(self, form):
        print("register form invalid")
        context = self.get_context_data()
        context['form'] = form
        context['error_message'] = 'Invalid form'
        return self.render_to_response(context)



    


# create a profile view
class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile/profile_get.html'
    context_object_name = 'user_object'

    # permissions user should have logged in to view this page
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return reverse_lazy('login')
        return super(ProfileView, self).get(request, *args, **kwargs)

    # find user by auth id
    def get_object(self):
        return get_user_model().objects.get(id=self.request.user.id)
                   


# create view to update profile
class ProfileUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'profile/profile_update.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('profile')

    # # if fails redirect to error page
    # def form_invalid(self, form):
    #     return reverse_lazy('error')

    # find user by auth id
    def get_object(self):
        return get_user_model().objects.get(id=self.request.user.id)

# create view for delete profile view
class ProfileDeleteView(DeleteView):
    model = get_user_model()
    template_name = 'profile/profile_delete.html'
    success_url = reverse_lazy('home')

    # find user by auth id
    def get_object(self):
        return get_user_model().objects.get(id=self.request.user.id)