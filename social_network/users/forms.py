from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

GENDER_CHOICES = [
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