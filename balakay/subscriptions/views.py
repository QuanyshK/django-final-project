from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Subscription


class SubscriptionListView(ListView):
    model = Subscription
    template_name = 'subscriptions/subscription_list.html'  
    context_object_name = 'subscriptions'

class SubscriptionDetailView(DetailView):
    model = Subscription
    template_name = 'subscriptions/subscription_detail.html'
    context_object_name = 'subscription'


class SubscriptionCreateView(CreateView):
    model = Subscription
    template_name = 'subscriptions/subscription_form.html'
    fields = ['active', 'name', 'price', 'duration_text', 'age_group', 'total_days', 'freeze_days', 'daily_visits', 'monthly_visits', 'premium_monthly_visits']


class SubscriptionUpdateView(UpdateView):
    model = Subscription
    template_name = 'subscriptions/subscription_form.html'
    fields = ['active', 'name', 'price', 'duration_text', 'age_group', 'total_days', 'freeze_days', 'daily_visits', 'monthly_visits', 'premium_monthly_visits']

class SubscriptionDeleteView(DeleteView):
    model = Subscription
    template_name = 'subscriptions/subscription_confirm_delete.html'
    success_url = reverse_lazy('subscription-list')
