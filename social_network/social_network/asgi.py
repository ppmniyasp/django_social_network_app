"""
ASGI config for social_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')


application = ProtocolTypeRouter({
    # Empty path for Django views
    "http": get_asgi_application(),
    # WebSocket path
    "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),  # Use your WebSocket routing here
})


# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path

# from chat.routing import websocket_urlpatterns  # Import your WebSocket routing from your app

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

# application = ProtocolTypeRouter({
#     # Empty path for Django views
#     "http": get_asgi_application(),
#     # WebSocket path
#     "websocket": URLRouter(websocket_urlpatterns),  # Use your WebSocket routing here
# })