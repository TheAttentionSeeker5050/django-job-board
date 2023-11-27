# login form using class based form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from users.models import CustomUser

# the form
class UserLoginForm(AuthenticationForm):
    """A form that logs a user in, with no privileges, from the given username and password."""
    # modify form style
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add placeholders and classes
        placeholders = {
            'username': 'Username',
            'password': 'Password',
        }

        # # set autofocus on first field
        # self.fields['username'].widget.attrs['autofocus'] = True

        # set placeholders and classes
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
            self.fields[field].widget.attrs['class'] = 'border-2 border-slate-800  rounded-lg outline-0 focus:border-purple-700 bg-purple-50 py-1 px-2'
            
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

# create account form using class based form
class RegisterForm(UserCreationForm):
    """A form that creates a user, with no privileges, from the given username and password."""

    # modify form style
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add placeholders and classes
        placeholders = {
            'username': 'Username',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

        # # set autofocus on first field
        # self.fields['username'].widget.attrs['autofocus'] = True

        # set placeholders and classes
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
            self.fields[field].widget.attrs['class'] = 'form-control border-2 border-slate-800 px-2 rounded-lg outline-0 focus:border-purple-700 bg-purple-50 py-1'

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']