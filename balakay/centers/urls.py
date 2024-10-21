from django.urls import path
from .views import *

urlpatterns = [
    path('home', home_view, name='home'),
    path('section/<int:id>', section_view),
    path('book/<int:schedule_id>/', book_schedule_view, name='book_schedule'),
    path('booking-success/', booking_success_view, name='booking_success'),
    path('my-schedule/', user_bookings, name='my-schedule'),
    path('cancel-booking/<int:booking_id>/', cancel_booking_view, name='cancel_booking'),
    path('centers/', center_list_view, name='center_list'), 
    path('user/bookings/', user_bookings, name='user_bookings'),
]
