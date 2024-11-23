from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth import login
from .forms import PartnerRegistrationForm, ScheduleForm
from centers.models import Schedule, Booking
from django.http import HttpResponseForbidden
from merchant.models import Partner
from django.contrib.auth.views import LoginView

class PartnerLoginView(LoginView):
    """
    Встроенное представление для авторизации партнера.
    """
    template_name = 'login_partner.html'


def register_partner(request):
    """
    Регистрация партнера.
    """
    if request.method == 'POST':
        form = PartnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            group, _ = Group.objects.get_or_create(name='Partners')
            user.groups.add(group)
            center = form.cleaned_data['center']
            Partner.objects.create(user=user, center=center)  # Сохранение выбранного центра
            return redirect('login_partner')  # Перенаправление на страницу входа
    else:
        form = PartnerRegistrationForm()
    return render(request, 'register_partner.html', {'form': form})




@login_required
def manage_schedule(request):
    """
    Управление расписанием партнера.
    """
    partner = request.user.partner
    if not partner.is_active:  # Проверка активации
        return HttpResponseForbidden("Your account is not active. Please contact the admin.")

    schedules = Schedule.objects.filter(section__center=partner.center)
    return render(request, 'manage_schedule.html', {'schedules': schedules})



@login_required
def add_schedule(request):
    """
    Добавление нового расписания.
    """
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.save()
            return redirect('manage_schedule')
    else:
        form = ScheduleForm()
    return render(request, 'add_schedule.html', {'form': form})

@login_required
def view_bookings(request):
    """
    Просмотр записей на секции партнера.
    """
    partner = request.user.partner
    if not partner.is_active:
        return HttpResponseForbidden("Your account is not active. Please contact the admin.")

    bookings = Booking.objects.filter(schedule__section__center=partner.center)
    return render(request, 'view_bookings.html', {'bookings': bookings})
