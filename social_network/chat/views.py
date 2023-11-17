from django.shortcuts import render, redirect
from .models import ChatModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from users.models import Profile
from post.utils import searchProfile

# Create your views here.

def chat(request):
    users = User.objects.exclude(username=request.user.username)
    profiles = Profile.objects.exclude(username=request.user.username)
    search_profile, search_query = searchProfile(request)
    user = User.objects.get(username=request.user.username)
    chat = ChatModel.objects.filter(read_status=False, receiver=user).exclude(sender=request.user.username).distinct()
    unread_users = [message.sender for message in chat]
    unique_unread_users = list(set(unread_users)) # removed dublicat item
    msg_cnt = len(unique_unread_users)
    context = {
        'users':users, 
        'profiles': profiles,
        'not_read_chat': unread_users, 
        'msg_cnt':msg_cnt,
        'search_profile': search_profile,
        'search_query': search_query
        }
    return render(request, 'chat/lobby.html', context)

def chatPage(request, username):
    chat_user=username
    user_object = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)
    profiles = Profile.objects.exclude(username=request.user.username)
    search_profile, search_query = searchProfile(request)
    my_profile =Profile.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(username=username)
    user = User.objects.get(username=request.user.username)
    chat = ChatModel.objects.filter(read_status=False, receiver=user).exclude(sender=request.user.username).distinct()
    unread_users = [message.sender for message in chat]
    unique_unread_users = list(set(unread_users))
    if username in unique_unread_users:
        unique_unread_users.remove(username) # removed dublicat item
    msg_cnt = len(unique_unread_users)

    if request.user.id > user_object.id:
        thread_name = f'chat_{request.user.id}-{user_object.id}'
    else:
        thread_name = f'chat_{user_object.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    messeges = ChatModel.objects.filter(thread_name=thread_name).exclude(receiver=user_object)   
    context = {
        'users':users,
        'user_profile':user_profile,
        'user':user_object,
        'profiles': profiles, 
        'messages':message_objs,
        'not_read_chat': unique_unread_users, 
        'msg_cnt':msg_cnt,
        'chat_user':chat_user,
        'my_profile':my_profile,
        'search_profile': search_profile,
        'search_query': search_query
        }
    return render(request, 'chat/main_chat.html', context)

