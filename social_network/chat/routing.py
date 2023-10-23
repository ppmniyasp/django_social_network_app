from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<id>\d+)/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/online/', consumers.OnlineStatusConsumer.as_asgi()),
]