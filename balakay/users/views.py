from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import ChildForm, UserLoginForm, ClientRegistrationForm, UserUpdateForm, ClientUpdateForm
from .models import *
from django.contrib.auth.decorators import login_required


def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login') 
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            return redirect('profile')  
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm(request)
    return render(request, 'users/login.html', {'form': form})  

def logout_user(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    client = Client.objects.get(user=request.user)
    children = Child.objects.filter(parent=client)
    active_subscriptions = UserSubscription.objects.filter(parent=client, expiration_date__gte=timezone.now())  # Фильтруем по полю parent и проверяем, что абонемент активен
    return render(request, 'users/profile.html', {
        'user': request.user,
        'client': client,
        'children': children,
        'active_subscriptions': active_subscriptions
    })

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
            return redirect('profile') 
    else:
        user_form = UserUpdateForm(instance=user)
        client_form = ClientUpdateForm(instance=client)

    context = {
        'user_form': user_form,
        'client_form': client_form,
    }
    return render(request, 'users/update_profile.html', context)  



def add_child_view(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = Client.objects.get(user=request.user)
            child.save()
            return redirect('profile') 
    else:
        form = ChildForm()
    
    return render(request, 'users/add_child.html', {'form': form})
