from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register-user/', views.registerUser, name='register-user'),
    path('edit-user/', views.editProfile, name='edit-user'),
    path('profile/', views.profile, name='profile'),
    path('users/', views.users, name='users')
]