from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'Registration successful. Please login.')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            response = redirect('home')
            response.set_cookie('access_token', str(refresh.access_token))
            response.set_cookie('refresh_token', str(refresh))
            return response
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
