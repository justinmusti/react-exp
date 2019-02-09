from django.contrib.auth import login as login_user, authenticate, logout as logout_user
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view


def login(request):
    return render(request, 'login.html', status=200)


def register(request):
    return render(request, 'register.html')


def logout(request):
    logout_user(request)
    return redirect('/')


@api_view(['POST'])
def login_do(request):
    status = False
    status_code = 500
    error = ''
    data = []

    try:
        post_data = request.data
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


@api_view(['POST'])
def register_do(request):
    status = False
    status_code = 500
    error = None
    data = dict()

    try:
        post_data = request.data
        username = post_data.get('username', None)
        password = post_data.get('password', None)
        # Validate fields
        assert username and len(username) > 3, "Username must be at least 4 characters."
        assert password and len(password) > 5, "Password must be at least 6 characters."
        # Assert unique username
        username = username.lower()
        assert not User.objects.filter(username=username).exists(), "This username is taken."
        # Move forward with new entry
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        # authenticate user
        auth_user = authenticate(request, username=username, password=password)
        assert auth_user, "Unable to authenticate your new account."
        # Login user
        login_user(request, auth_user)
        status = True
        error = None
        status_code = 201
        data = {}
    except AssertionError as ae:
        status = False
        error = str(ae)
        data = {}
        status_code = 400

    except Exception as e:
        import traceback
        traceback.print_exc()
        status = False
        status_code = 500
        error = 'Something went wrong.'
        data = {}

    response_data = {
        'status': status,
        'error': error,
        'data': data
    }
    return JsonResponse(data=response_data, status=status_code)

