from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register_partner, manage_schedule, add_schedule, view_bookings, PartnerLoginView

urlpatterns = [
    path('register/', register_partner, name='register_partner'),
    path('schedule/', manage_schedule, name='manage_schedule'),
    path('schedule/add/', add_schedule, name='add_schedule'),
    path('bookings/', view_bookings, name='view_bookings'),
    path('login/', PartnerLoginView.as_view(), name='login_partner'),  # Авторизация

]
