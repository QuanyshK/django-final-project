from django.urls import path
from .views import *

urlpatterns = [
    path('home', home_view, name='home'),
    path('section/<int:id>/', section_view, name='section'),
    path('book/<int:schedule_id>/', book_schedule_view, name='book_schedule'),
    path('booking-success/', booking_success_view, name='booking_success'),
    path('my-schedule/', user_bookings, name='my-schedule'),
    path('cancel-booking/<int:booking_id>/', cancel_booking_view, name='cancel_booking'),
    path('user/bookings/', user_bookings, name='user_bookings'),
    path('center/<int:center_id>/', center_details, name='center_details'),
    path('booking/<int:booking_id>/', booking_detail, name='booking_detail'),
    path('section/<int:id>/add_favorite/', add_favorite_section, name='add_favorite_section'),
    path('section/<int:id>/remove_favorite/', remove_favorite_section, name='remove_favorite_section'),
    path('favorites/', favorite_sections_view, name='favorite_sections'),
    path('past-bookings/', past_bookings_view, name='past_bookings'),
]
