from django.urls import path
from .views import (
    login,
    login_do
)


app_name = 'user'
urlpatterns = [
    path('login/', login, name='login'),
    path('login-do/', login_do, name='login_do'),
]
