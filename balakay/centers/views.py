from datetime import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Section, Center, Schedule, Category, Booking
from .forms import BookingForm


# Create your views here.


def home_view(request):
    categories = Category.objects.prefetch_related('sections').all()
    return render(request, 'home.html', {'categories': categories})

def section_view(request, id):
    section = Section.objects.get(id=id)
    schedules = Schedule.objects.filter(section=section)
    return render(request, 'section.html', {"section": section, "schedules": schedules})


def book_schedule_view(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.schedule = schedule
            booking.user = request.user
            booking.save()
            return redirect(reverse('booking_success'))
    else:
        form = BookingForm()

    return render(request, 'book_schedule.html', {'form': form, 'schedule': schedule})

def booking_success_view(request):
    return render(request, 'booking_success.html')


def my_bookings_view(request):
    # Assuming 'parent_phone' or similar can be used to identify the current user (adjust according to your auth system)
    parent_phone = request.user.profile.phone_number  # Adjust this to match your user data
    
    active_bookings = Booking.objects.filter(parent_phone=parent_phone, status__in=[Booking.PENDING, Booking.CONFIRMED])

    return render(request, 'my_schedule.html', {'active_bookings': active_bookings})

def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.status == Booking.PENDING:
        booking.status = Booking.CANCELLED
        booking.cancelled_at = timezone.now()
        booking.save()

    return redirect('my-schedule')