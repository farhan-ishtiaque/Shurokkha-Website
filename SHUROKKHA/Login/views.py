from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Task,TaskSerializer
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserIDLoginForm
from police.forms import PoliceStationForm
from police.models import  PoliceStation
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer
from firestation.models import FireStation
from firestation.forms import FireStationForm

@login_required
def add_fire_station(request):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    if request.method == 'POST':
        form = FireStationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.password = "fire123"
            station.save()
            return redirect('fire_station_list')
    else:
        form = FireStationForm()
    return render(request, 'login/add_fire_station.html', {'form': form})

@login_required
def fire_station_list(request):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    stations = FireStation.objects.all()
    return render(request, 'login/fire_station_list.html', {'stations': stations})

# Admin operator functions
@login_required
def operator_dashboard(request):
    return render(request, 'login/operator_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'login/admin_dashboard.html')

@login_required
def redirect_user(request):
    user = request.user
    if hasattr(user, 'role'):
        if user.role == 'operator':
            return redirect('operator_dashboard')
        elif user.role == 'admin':
            return redirect('admin_dashboard')
    return redirect('login')

@login_required
def add_operator(request):
    last_user = User.objects.order_by('-id').first()
    next_user_id = last_user.id + 1 if last_user else 1000

    if request.user.role != 'admin':
        return redirect('redirect_user')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            operator = form.save(commit=False)
            operator.user_id = next_user_id
            operator.role = 'operator'
            operator.set_password("operator123")  # Default password
            operator.save()
            return redirect('operator_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'login/add_operator.html', {'form': form, 'next_user_id': next_user_id})

@login_required
def operator_list(request):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    operators = User.objects.filter(role='operator')
    return render(request, 'login/operator_list.html', {'operators': operators})

@login_required
def edit_operator(request, user_id):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    operator = get_object_or_404(User, pk=user_id, role='operator')
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=operator)
        if form.is_valid():
            form.save()
            return redirect('operator_list')
    else:
        form = CustomUserChangeForm(instance=operator)
    return render(request, 'login/edit_operator.html', {'form': form, 'operator': operator})

@login_required
def delete_operator(request, user_id):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    operator = get_object_or_404(User, pk=user_id, role='operator')
    operator.is_active = not operator.is_active
    operator.save()
    return redirect('operator_list')

@login_required
def set_password(request, user_id):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    operator = get_object_or_404(User, pk=user_id, role='operator')
    if request.method == 'POST':
        form = SetPasswordForm(operator, request.POST)
        if form.is_valid():
            form.save()
            return redirect('operator_list')
    else:
        form = SetPasswordForm(operator)
    return render(request, 'login/set_password.html', {'form': form, 'operator': operator})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '✅ Your password was successfully updated!')
            return redirect('operator_dashboard')
        else:
            messages.error(request, '⚠ Please correct the error below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'login/change_password.html', {'form': form})

# Login view
def custom_login(request):
    if request.method == 'POST':
        form = UserIDLoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            user = authenticate(request, username=str(user_id), password=password)
            if user and user.is_active:
                auth_login(request, user)
                return redirect('redirect_user')
            else:
                form.add_error(None, 'Invalid user ID or password')
    else:
        form = UserIDLoginForm()
    return render(request, 'login/login.html', {'form': form})

@login_required
def search_list(request):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    division_query = request.GET.get('division')
    if division_query:
        operators = User.objects.filter(role='operator', division__iexact=division_query)
    else:
        operators = User.objects.filter(role='operator')
    return render(request, 'login/search_list.html', {
        'operators': operators,
        'selected_division': division_query or ''
    })


# Police Station Management
@login_required
def add_police_station(request):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    if request.method == 'POST':
        form = PoliceStationForm(request.POST)
        if form.is_valid():
            station = form.save(commit=False)
            station.password = "police123"
            station.save()
            return redirect('police_station_list')
    else:
        form = PoliceStationForm()
    return render(request, 'login/add_station.html', {'form': form})

@login_required
def police_station_list(request):
    if request.user.role != 'admin':
        return redirect('redirect_user')
    stations = PoliceStation.objects.all()
    return render(request, 'login/station_list.html', {'stations': stations})

# REST API
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


def live_map_view(request):
    return render(request, 'login/live_map.html')