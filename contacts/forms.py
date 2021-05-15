from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class addUserContact(ModelForm):
    class Meta:
        model=UserContacts
        fields=["full_name"]