from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


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
            return redirect('profile')
        else:
            messages.error(request,'username or password is incorrect..')

    return render(request, 'users/login-register.html')

def logoutProfile(request):
    logout(request)
    messages.error(request,'user was loged out..')
    return redirect('login')

def profile(request):
    return render(request, 'users/profile.html')