from django.core.exceptions import ValidationError
from django.utils import timezone
from notifications.models import Notification

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import PartnerRegistrationForm, ScheduleForm
from centers.models import Schedule, Booking, Section
from .models import Partner
from django.utils.timezone import now, timedelta
from django.contrib import messages


def register_partner(request):
    """
    Регистрация нового партнера.
    """
    if request.method == 'POST':
        form = PartnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            center = form.cleaned_data['center']
            Partner.objects.create(user=user, center=center)
            return redirect('login_partner')
    else:
        form = PartnerRegistrationForm()
    return render(request, 'register_partner.html', {'form': form})


def login_partner(request):
    """
    Авторизация партнера.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                if user.partner.is_active:
                    login(request, user)
                    return redirect('manage_schedule')
                else:
                    return render(request, 'login_partner.html', {'error': 'Ваш аккаунт не активирован.'})
            except Partner.DoesNotExist:
                return render(request, 'login_partner.html', {'error': 'Пользователь не является партнером.'})
        else:
            return render(request, 'login_partner.html', {'error': 'Неправильное имя пользователя или пароль.'})
    return render(request, 'login_partner.html')


@login_required
def manage_schedule(request):
    """
    Отображение всех расписаний партнера.
    """
    try:
        partner = request.user.partner
        if not partner.is_active:
            return redirect('login_partner')
    except Partner.DoesNotExist:
        return redirect('login_partner')

    sections = Section.objects.filter(center=partner.center)
    schedules = Schedule.objects.filter(section__in=sections)
    return render(request, 'manage_schedule.html', {'schedules': schedules})


@login_required
@user_passes_test(lambda u: hasattr(u, 'partner') and u.partner.is_active, login_url='/merchant/login/')
def schedule_details(request, schedule_id):
    """
    Отображает подробности расписания для партнера и список бронирований.
    """
    partner = request.user.partner
    sections = Section.objects.filter(center=partner.center)
    schedule = get_object_or_404(Schedule, id=schedule_id, section__in=sections)

    # Фильтрация бронирований
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = Booking.objects.filter(schedule=schedule, status=status_filter)
    else:
        bookings = Booking.objects.filter(schedule=schedule)

    # Расчет количества свободных мест
    available_slots = schedule.total_slots - bookings.count()

    statuses = Booking.STATUS_CHOICES
    return render(
        request,
        'schedule_details.html',
        {
            'schedule': schedule,
            'bookings': bookings,
            'statuses': statuses,
            'available_slots': available_slots,
        }
    )
@login_required
@user_passes_test(lambda u: hasattr(u, 'partner') and u.partner.is_active, login_url='/merchant/login/')
def add_schedule(request):
    partner = request.user.partner
    sections_queryset = Section.objects.filter(center=partner.center)  # Только секции текущего партнера

    if request.method == 'POST':
        form = ScheduleForm(request.POST, sections_queryset=sections_queryset)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            messages.success(request, "Schedule successfully added!")
            return redirect('manage_schedule')
    else:
        form = ScheduleForm(sections_queryset=sections_queryset)

    return render(request, 'add_schedule.html', {'form': form})


@login_required
def edit_schedule(request, schedule_id):
    partner = request.user.partner
    sections = Section.objects.filter(center=partner.center)
    schedule = get_object_or_404(Schedule, id=schedule_id, section__in=sections)

    if request.method == 'POST':
        if 'toggle_status' in request.POST and schedule.status == Schedule.ACTIVE:
            schedule.status = Schedule.CANCELLED
            schedule.save()
            messages.success(request, "Schedule has been cancelled and cannot be reactivated.")
            return redirect('manage_schedule')

        form = ScheduleForm(request.POST, instance=schedule, sections_queryset=sections)
        if form.is_valid():
            form.save()
            messages.success(request, "Schedule successfully updated!")
            return redirect('manage_schedule')
    else:
        form = ScheduleForm(instance=schedule, sections_queryset=sections)

    return render(request, 'edit_schedule.html', {'form': form, 'schedule': schedule})



@login_required
@user_passes_test(lambda u: hasattr(u, 'partner') and u.partner.is_active, login_url='/merchant/login/')
def center_profile(request):
    partner = request.user.partner
    center = partner.center  # Предполагается, что партнер привязан к одному центру
    return render(request, 'center_profile.html', {'center': center})

def create_notification(user, booking, message):
    Notification.objects.create(user=user, booking=booking, message=message)


@login_required
@user_passes_test(lambda u: hasattr(u, 'partner') and u.partner.is_active, login_url='/merchant/login/')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, schedule__section__center=request.user.partner.center)

    if booking.status == Booking.CANCELLED:
        messages.error(request, "This booking has already been cancelled.")
        return redirect('schedule_details', schedule_id=booking.schedule.id)

    booking.status = Booking.CANCELLED
    booking.cancelled_at = timezone.now()
    booking.save()

    message = f"Your booking for {booking.schedule.section.name} on {booking.schedule.start_time} has been cancelled by the partner."
    create_notification(user=booking.user, booking=booking, message=message)

    messages.success(request, f"Booking for {booking.child_name} successfully cancelled.")
    return redirect('schedule_details', schedule_id=booking.schedule.id)

from .serializers import SectionSerializer, ScheduleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class SectionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.contrib.auth import logout

def logout_partner(request):
    logout(request)
    return redirect('login_partner')