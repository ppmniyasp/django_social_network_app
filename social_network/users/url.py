from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginProfile, name="login"),
    path('logout/',views.logoutProfile, name="logout"),

    path('profile/', views.profile, name="profile")
]