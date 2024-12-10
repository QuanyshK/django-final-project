from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from .models import Client, Child, UserSubscription
from .serializers import ClientSerializer, ChildSerializer, UserSubscriptionSerializer
from .forms import ClientRegistrationForm, UserLoginForm, UserUpdateForm, ClientUpdateForm, ChildForm
from django.http import JsonResponse
from notifications.models import Notification
def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        messages.error(request, "Invalid credentials.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


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


@login_required
def profile_view(request):
    client = get_object_or_404(Client, user=request.user)
    children = Child.objects.filter(parent=client)
    active_subscriptions = UserSubscription.objects.filter(parent=client, expiration_date__gte=timezone.now())
    return render(request, 'users/profile.html', {'client': client, 'children': children, 'active_subscriptions': active_subscriptions})

@login_required
def update_profile(request):
    user = request.user
    client = get_object_or_404(Client, user=user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        client_form = ClientUpdateForm(request.POST, instance=client)
        if user_form.is_valid() and client_form.is_valid():
            user_form.save()
            client_form.save()
            client.refresh_from_db()
            return JsonResponse({'message': 'Profile updated successfully!'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid data submitted'}, status=400)
    else:
        user_form = UserUpdateForm(instance=user)
        client_form = ClientUpdateForm(instance=client)
    return render(request, 'users/update_profile.html', {'user_form': user_form, 'client_form': client_form})




@login_required
def add_child_view(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.parent = get_object_or_404(Client, user=request.user)
            child.save()
            return JsonResponse({'message': 'Child added successfully!'}, status=201)  
    else:
        form = ChildForm()
    return render(request, 'users/add_child.html', {'form': form})


@login_required
def subscription_detail(request, id):
    client = get_object_or_404(Client, user=request.user)
    user_subscription = get_object_or_404(UserSubscription, id=id, parent=client)
    if user_subscription.is_active:
        user_subscription.update_remaining_days_and_visits()
    return render(request, 'users/subscription_detail.html', {'user_subscription': user_subscription})
@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/user_notifications.html', {'notifications': notifications})


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]


class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
