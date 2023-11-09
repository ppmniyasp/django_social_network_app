from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('new-post/',views.new_post, name="new-post"),
    path('post-details/<str:pk>/', views.post_details, name="post-details"),
    path('like/<str:pk>/', views.like, name='like'),
    path('tag/<str:slug>',views.tag, name="tag"),
    path('favourite/<str:pk>/',views.favourite, name="favourite"),
    path('follow/<str:username>/<option>/', views.follow, name="follow")
]