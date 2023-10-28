from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='chat_rooms')

    def __str__(self):
        return self.name

class Message(models.Model):
    content = models.TextField( null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=(("unread", "Unread"), ("read", "Read")), default="unread")

    def __str__(self):
        return f"Message from {self.sender} in {self.chat_room.name}"


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    name = models.CharField(max_length=100, null=True, blank=True)  # Chat name or title
    last_message = models.TextField( null=True, blank=True)  # Last message content
    last_message_timestamp = models.DateTimeField(null=True, blank=True)  # Timestamp of the last message
    unread_message_count = models.PositiveIntegerField(default=0)  # Number of unread messages

    def __str__(self):
        return self.name
    


class ChatModel(models.Model):
    sender = models.CharField(max_length=100, default=None)
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="messeges")
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.message