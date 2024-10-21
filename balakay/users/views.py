from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, ClientRegistrationForm,UserUpdateForm,ClientUpdateForm
from .models import User,Client
from django.contrib.auth.decorators import login_required


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

@login_required
def profile_view(request):
    client = request.user.client 
    return render(request, 'profile.html', {'client': client})


@login_required
def update_profile(request):
    user = request.user
    client = Client.objects.get(user=user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        client_form = ClientUpdateForm(request.POST, instance=client)
        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            return redirect('profile')  # Redirect to profile page after successful update
    else:
        user_form = UserUpdateForm(instance=user)
        client_form = ClientUpdateForm(instance=client)

    context = {
        'user_form': user_form,
        'client_form': client_form,
    }
    return render(request, 'update_profile.html', context)