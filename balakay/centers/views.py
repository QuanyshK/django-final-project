from datetime import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Section, Center, Schedule, Category, Booking
from .forms import BookingForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

def home_view(request):
    categories = Category.objects.prefetch_related('sections').all()
    return render(request, 'centers/home.html', {'categories': categories})

def section_view(request, id):
    section = get_object_or_404(Section, id=id)  
    schedules = Schedule.objects.filter(section=section)
    return render(request, 'centers/section.html', {"section": section, "schedules": schedules})

def book_schedule_view(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)  
        if form.is_valid():
            booking = form.save(commit=False)
            booking.schedule = schedule
            booking.user = request.user
            booking.child = form.cleaned_data['child']  
            booking.save()
            schedule.total_slots -= 1
            schedule.save()  
            return redirect(reverse('booking_success'))
    else:
        form = BookingForm(user=request.user) 

    return render(request, 'centers/book_schedule.html', {'form': form, 'schedule': schedule})

def booking_success_view(request):
    return render(request, 'centers/booking_success.html')



def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.status == Booking.PENDING:
        booking.status = Booking.CANCELLED
        booking.cancelled_at = timezone.now()
        booking.save()

    return redirect('my-schedule')

def center_list_view(request):
    query = request.GET.get('q', '')  

    centers = Center.objects.all() 
    if query:
        centers = centers.filter(Q(name__icontains=query) | Q(id__icontains=query))

    return render(request, 'centers/center_list.html', {
        'centers': centers,
        'query': query,   
    })
    
@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('schedule')
    return render(request, 'centers/my_schedule.html', {'bookings': bookings})

def center_details(request, center_id):
    center = get_object_or_404(Center, id=center_id)
    schedules = Schedule.objects.filter(section__center=center)
    
    return render(request, 'centers/center_details.html', {'center': center, 'schedules': schedules})


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm':
            booking.status = Booking.CONFIRMED
            booking.confirmed_at = timezone.now()
        elif action == 'cancel':
            booking.status = Booking.CANCELLED
            booking.cancelled_at = timezone.now()
        
        booking.save()
        return redirect(reverse('booking_detail', args=[booking.id]))

    return render(request, 'centers/booking_detail.html', {'booking': booking})