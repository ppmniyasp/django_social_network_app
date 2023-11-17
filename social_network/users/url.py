from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginProfile, name="login"),
    path('logout/',views.logoutProfile, name="logout"),
    path('register-page/',views.registerProfile, name="register"),

    path('profile/<str:username>/', views.profile, name="profile"),
    path('profilefavourite/<str:username>/', views.profile, name="profilefavourite"),
    path('edit-profile', views.edit_profile, name="edit-profile")
]