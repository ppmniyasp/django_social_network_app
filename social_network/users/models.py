from django.db import models
import uuid
from post.models import Post
from django.contrib.auth.models import User


# Create your models here.

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank= True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=30, null=True, blank=True, choices=GENDER_CHOICES)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    online_status = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to='profiles/', default="profiles/defaudt.jpg", null=True,blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    favourite = models.ManyToManyField(Post, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
