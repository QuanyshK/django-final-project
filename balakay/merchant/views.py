from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import PartnerRegistrationForm, ScheduleForm
from centers.models import Schedule, Booking, Section
from .models import Partner


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
def schedule_details(request, schedule_id):
    """
    Отображение деталей расписания (кто записался).
    """
    try:
        partner = request.user.partner
        if not partner.is_active:
            return redirect('login_partner')
    except Partner.DoesNotExist:
        return redirect('login_partner')

    # Проверяем, что расписание связано с секциями партнера
    sections = Section.objects.filter(center=partner.center)
    schedule = get_object_or_404(Schedule, id=schedule_id, section__in=sections)
    bookings = Booking.objects.filter(schedule=schedule)
    return render(request, 'view_bookings.html', {'schedule': schedule, 'bookings': bookings})


@login_required
@user_passes_test(lambda u: hasattr(u, 'partner') and u.partner.is_active, login_url='/merchant/login/')
def add_schedule(request):
    partner = request.user.partner
    sections = Section.objects.filter(center=partner.center)  # Получаем секции, принадлежащие центру партнера

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            section_id = request.POST.get('section')  # Получаем выбранную секцию из POST-запроса
            try:
                schedule.section = sections.get(id=section_id)  # Проверяем, что секция относится к партнеру
                schedule.save()
                return redirect('manage_schedule')
            except Section.DoesNotExist:
                form.add_error('section', 'Invalid section for your center.')
    else:
        form = ScheduleForm()
        form.fields['section'].queryset = sections  # Ограничиваем выбор секций только центром партнера

    return render(request, 'add_schedule.html', {'form': form})

@login_required
def edit_schedule(request, schedule_id):
    """
    Редактирование существующего расписания.
    """
    try:
        partner = request.user.partner
        if not partner.is_active:
            return redirect('login_partner')
    except Partner.DoesNotExist:
        return redirect('login_partner')

    sections = Section.objects.filter(center=partner.center)
    schedule = get_object_or_404(Schedule, id=schedule_id, section__in=sections)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('manage_schedule')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'edit_schedule.html', {'form': form})
