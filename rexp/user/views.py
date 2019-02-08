from django.contrib.auth import login as login_user, authenticate, logout as logout_user
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json


def login(request):
    return render(request, 'login.html')


def logout(request):
    logout_user(request)
    return redirect('/')


def login_do(request):
    status = False
    status_code = 500
    error = ''
    data = []

    try:
        # Convert and capture form data
        post_data = json.loads(request.body)
        username = post_data.get('username', None)
        password = post_data.get('password', None)
        # Ensure required fields are not empty and expected length
        assert username and len(username) > 3, "Username must be 4 or more characters"
        assert password and len(password) > 6, "Password must be 7 or more characters"
        username = username.lower()
        # Ensure user object exists with given username
        assert User.objects.filter(username=username).exists(), 'No account with given username.'

        # Validate credentials
        user = authenticate(request, username=username, password=password)
        assert user, "Wrong Credentials"
        # Login User
        login_user(request=request, user=user)
        status = True
        status_code = 200
        error = ''
        data = dict()

    except AssertionError as ae:
        status_code = 400
        status = False
        error = str(ae)
        data = {}
    except Exception as e:
        status = False
        status_code = 500
        error = 'Something went wrong'
        data = {}


    return_data = {
        'status': status,
        'error': error,
        'data': data
    }
    return JsonResponse(data=return_data, status=status_code)
