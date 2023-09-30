# login form using class based form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

# the form
class UserLoginForm(AuthenticationForm):
    """A form that logs a user in, with no privileges, from the given username and password."""
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

# create account form using class based form
class RegisterForm(UserCreationForm):
    """A form that creates a user, with no privileges, from the given username and password."""
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']