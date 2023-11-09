from django.shortcuts import render, redirect
from .models import ChatModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def chat(request):
    users = User.objects.exclude(username=request.user.username)
    user = User.objects.get(username=request.user.username)
    chat = ChatModel.objects.filter(read_status=False, receiver=user).exclude(sender=request.user.username).distinct()
    unread_users = [message.sender for message in chat]
    unique_unread_users = list(set(unread_users)) # removed dublicat item
    msg_cnt = len(unique_unread_users)
    print('un read read',unread_users)
    print('not read',msg_cnt)
    context = {'users':users,'not_read_chat': unread_users, 'msg_cnt':msg_cnt}
    return render(request, 'chat/lobby.html', context)

def chatPage(request, username):
    user_object = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)

    if request.user.id > user_object.id:
        thread_name = f'chat_{request.user.id}-{user_object.id}'
    else:
        thread_name = f'chat_{user_object.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    messeges = ChatModel.objects.filter(thread_name=thread_name).exclude(receiver=user_object)
    # for msg in messeges:
    #     print('messege',msg,username)
    #     msg.read_status = True
    #     msg.save()
    # chat = ChatModel.objects.get(sender=username)
    # chat.read_status = True    
    context = {'users':users,'user':user_object, 'messages':message_objs}
    return render(request, 'chat/main_chat.html', context)

