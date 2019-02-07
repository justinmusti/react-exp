from django.urls import path
from .views import login


app_name = 'user'
urlpatterns = [
    path('login/', login, name='login'),
]
