from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat),
    path('chat-page/<str:username>/', views.chatPage, name="chat-page")
]