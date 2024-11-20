from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home_view,
    section_view,
    book_schedule_view,
    booking_success_view,
    user_bookings,
    center_details,
    add_favorite_section,
    remove_favorite_section,
    favorite_sections_view,
    past_bookings_view,
    CategoryViewSet,
    CenterViewSet,
    SectionViewSet,
    ScheduleViewSet,
    BookingViewSet,
    FavoriteSectionViewSet,
)



router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'centers', CenterViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'favorites', FavoriteSectionViewSet)

urlpatterns = [
    path('home/', home_view, name='home'),
    path('section/<int:id>/', section_view, name='section'),
    path('section/<int:id>/add-favorite/', add_favorite_section, name='add_favorite_section'),
    path('section/<int:id>/remove-favorite/', remove_favorite_section, name='remove_favorite_section'),
    path('center/<int:center_id>/', center_details, name='center_details'),
    path('book/<int:schedule_id>/', book_schedule_view, name='book_schedule'),
    path('booking-success/', booking_success_view, name='booking_success'),
    path('my-schedule/', user_bookings, name='my_schedule'),
    path('favorites/', favorite_sections_view, name='favorite_sections'),
    path('past-bookings/', past_bookings_view, name='past_bookings'),
    path('', include(router.urls)),
]
