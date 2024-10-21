from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, ClientRegistrationForm
from .models import User

def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')  # Redirect to a login page after successful registration
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'register.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)  # Pass request to the form
        if form.is_valid():
            # Get the authenticated user
            user = form.get_user()
            login(request, user) 
            return redirect('/')  # Redirect to home or another page after login
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm(request)
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')
