from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserFile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User # Use Django's built-in User model
        fields = ('username', 'password1', 'password2') # Fields to be included in the form

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file']