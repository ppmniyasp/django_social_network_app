from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name="chats"),
    path('chat-page/<str:username>/', views.chatPage, name="chat-page")
]