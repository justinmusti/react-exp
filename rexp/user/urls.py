from django.urls import path
from .views import (
    login,
    login_do,
    logout
)


app_name = 'user'
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('login-do/', login_do, name='login_do'),
]
