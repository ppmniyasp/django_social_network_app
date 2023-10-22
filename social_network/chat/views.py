from django.shortcuts import render, redirect
from .models import ChatRoom, Message,ChatModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def chat(request):
    users = User.objects.exclude(username=request.user.username)
    context = {'users':users}
    return render(request, 'chat/lobby.html', context)

def chatPage(request, username):
    user_object = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)

    if request.user.id > user_object.id:
        thread_name = f'chat_{request.user.id}-{user_object.id}'
    else:
        thread_name = f'chat_{user_object.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    context = {'users':users,'user':user_object, 'messages':message_objs}
    return render(request, 'chat/main_chat.html', context)

@login_required(login_url='profile')
def chat_room_view(request, chat_room_id):
    chat_room = ChatRoom.objects.get(id=chat_room_id)
    messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('message_content')
        sender = request.user
        status = 'unread'  # Set the initial status to 'unread'
        message = Message(content=content, sender=sender, chat_room=chat_room, status=status)
        message.save()
        return redirect('chat_room', chat_room_id=chat_room_id)

    return render(request, 'chat/lobby.html', {'chat_room': chat_room, 'messages': messages})
