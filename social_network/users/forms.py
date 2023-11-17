from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

GENDER_CHOICES = [
    ('', '----------'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

class EditProfileForm(forms.ModelForm):
    profile_img = forms.ImageField(required=True)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Email'}), required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'input'}), required=True)
    social_website = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'www.mywebsite.com'}), required=True)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Address'}), required=True)

    class Meta:
        model = Profile
        fields = ['profile_img', 'name', 'email', 'bio', 'gender','social_website', 'location']
        labels = {
            'profile_img': 'Profile'
        }


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Full Name'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Email'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm Password'}), required=True)

    class Meta:
        model=User
        fields = ['first_name','username','email','password1','password2'] 
        labels = {
            'first_name': 'Full Name'
        }