from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import Profile
from post.models import Post, Follow
from .forms import EditProfileForm



# Create your views here.

def loginProfile(request):

    # if request.user.is_authenticated:
    #     return redirect('')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request,'username does not exist..')


        # this will check username match the password if it is it return a instance else none
        user = authenticate(request, username=username, password=password )

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request,'username or password is incorrect..')

    return render(request, 'users/login-register.html')

def logoutProfile(request):
    logout(request)
    messages.error(request,'user was loged out..')
    return redirect('login')

def profile(request, username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favourite.all()

    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    # pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'profile':profile,
        'posts_count':posts_count,
        'following_count':following_count,
        'followers_count':followers_count,
        'posts_paginator':posts_paginator,
        'follow_status':follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, 'users/profile.html',context)

def edit_profile(request):
    user = request.user.id
    profile = get_object_or_404(Profile, user__id=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.profile_img = form.cleaned_data.get('profile_img')
            profile.name = form.cleaned_data.get('name')
            profile.email = form.cleaned_data.get('email')
            profile.gender = form.cleaned_data.get('gender')
            profile.location = form.cleaned_data.get('location')
            profile.social_website = form.cleaned_data.get('social_website')
            profile.bio = form.cleaned_data.get('bio')
            profile.save() 
            return redirect('profile', profile.username)
        else:
            print("------something wrong-----")
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
    }
    return render(request, 'users/edit_profile.html', context)

# def EditProfile(request):
#     user = request.user.id
#     profile = Profile.objects.get(user__id=user)

#     if request.method == "POST":
#         form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if form.is_valid():
#             profile.image = form.cleaned_data.get('image')
#             profile.first_name = form.cleaned_data.get('first_name')
#             profile.last_name = form.cleaned_data.get('last_name')
#             profile.location = form.cleaned_data.get('location')
#             profile.url = form.cleaned_data.get('url')
#             profile.bio = form.cleaned_data.get('bio')
#             profile.save()
#             return redirect('profile', profile.user.username)
#     else:
#         form = EditProfileForm(instance=request.user.profile)

#     context = {
#         'form':form,
#     }
#     return render(request, 'editprofile.html', context)

