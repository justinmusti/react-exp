from django.urls import path
from .views import (
    login,
    login_do,
    logout,
    register,
    register_do,
)


app_name = 'user'
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('register-do/', register_do, name='register_do'),
    path('login-do/', login_do, name='login_do'),
]
