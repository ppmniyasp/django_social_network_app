from django.db import models
from django.contrib.auth.models import User
    

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