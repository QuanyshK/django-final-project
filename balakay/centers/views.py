from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Section, Center, Schedule, Category, Booking, FavoriteSection
from .forms import BookingForm

def home_view(request):
    query = request.GET.get("q", "")
    search_type = request.GET.get("search_type", "all")
    category_id = request.GET.get("category", "")

    centers = Center.objects.none()
    sections = Section.objects.none()
    categories = Category.objects.all()

    if search_type == "centers" or search_type == "all":
        centers = Center.objects.filter(name__icontains=query)

    if search_type == "sections" or search_type == "all":
        sections = Section.objects.filter(name__icontains=query)
        if category_id:
            sections = sections.filter(category__id=category_id)
    centers_paginator = Paginator(centers, 10)  
    centers_page_number = request.GET.get('page')
    centers_page = centers_paginator.get_page(centers_page_number)
    sections_paginator = Paginator(sections, 10) 
    sections_page_number = request.GET.get('page')
    sections_page = sections_paginator.get_page(sections_page_number)

    return render(request, "centers/home.html", {
        "query": query,
        "search_type": search_type,
        "category_id": category_id,
        "centers": centers_page,
        "sections": sections_page,
        "categories": categories
    })
def section_view(request, id):
    section = get_object_or_404(Section, id=id)
    schedules = Schedule.objects.filter(section=section, start_time__gte=timezone.now()).order_by('start_time')
    paginator = Paginator(schedules, 5)
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = request.user.client.favoritesection_set.filter(section=section).exists()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'centers/section.html', {"section": section, "page_obj": page_obj, "schedules": schedules, 'is_favorited': is_favorited,})

def book_schedule_view(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    existing_bookings = Booking.objects.filter(schedule=schedule, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user, section=schedule.section)
        if form.is_valid():
            if existing_bookings.exists():
                form.add_error(None, 'You have already booked this schedule for this child.')
            else:
                booking = form.save(commit=False)
                booking.schedule = schedule
                booking.user = request.user
                booking.save()
                schedule.total_slots -= 1
                schedule.save()
                return redirect(reverse('booking_success'))
    else:
        form = BookingForm(user=request.user, section=schedule.section)
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
@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user, schedule__start_time__gte=timezone.now()).select_related('schedule').order_by('schedule__start_time')
    paginator = Paginator(bookings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'centers/my_schedule.html', {'page_obj': page_obj, 'bookings': bookings})

def center_details(request, center_id):
    center = get_object_or_404(Center, id=center_id)
    sections = Section.objects.filter(center=center).order_by('name')
    paginator = Paginator(sections, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'centers/center_details.html', {'center': center, 'page_obj': page_obj, 'sections': sections})

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    schedule = booking.schedule
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm':
            booking.status = Booking.CONFIRMED
            booking.confirmed_at = timezone.now()
        elif action == 'cancel':
            booking.status = Booking.CANCELLED
            booking.cancelled_at = timezone.now()
            schedule.total_slots += 1
            schedule.save()
        booking.save()
        return redirect(reverse('booking_detail', args=[booking.id]))
    return render(request, 'centers/booking_detail.html', {'booking': booking})

@login_required
def add_favorite_section(request, id):
    section = get_object_or_404(Section, id=id)
    client = request.user.client
    favorite, created = FavoriteSection.objects.get_or_create(client=request.user.client, section=section)
    
    if created:
        return redirect('section', id=id)
    else:
        favorite.delete()
        return redirect('section', id=id)

@login_required
def remove_favorite_section(request, id):
    section = get_object_or_404(Section, id=id)
    client = request.user.client
    FavoriteSection.objects.filter(client=client, section=section).delete()
    return redirect('favorite_sections')

@login_required
def favorite_sections_view(request):
    client = request.user.client
    favorite_sections = FavoriteSection.objects.filter(client=client).select_related('section').order_by('section__name')
    paginator = Paginator(favorite_sections, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'centers/favorite_sections.html', {'page_obj': page_obj, 'favorite_sections': favorite_sections})

@login_required
def past_bookings_view(request):
    past_bookings = Booking.objects.filter(
        user=request.user,
        schedule__start_time__lt=timezone.now()
    ).order_by('-schedule__start_time')
    paginator = Paginator(past_bookings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'centers/past_bookings.html', {'page_obj': page_obj, 'past_bookings': past_bookings})
