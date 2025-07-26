from django.shortcuts import render, redirect
from .models import PoliceStation
from django.contrib import messages
from police.forms import PoliceStationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

def police_change_password(request):
    station_id = request.session.get('station_id')
    if not station_id:
        return redirect('police_login')

    station = PoliceStation.objects.get(station_id=station_id)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if station.password != current_password:
            messages.error(request, "Current password is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            station.password = new_password
            station.save()
            messages.success(request, "Password updated successfully.")
            return redirect('police_dashboard')

    return render(request, 'police/change_password.html', {'station': station})
def police_login_view(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        password = request.POST.get('password')

        try:
            station = PoliceStation.objects.get(station_id=station_id)
            if station.password == password:
                request.session['station_id'] = station.station_id
                request.session['station_name'] = station.name
                return redirect('police_dashboard')
            else:
                messages.error(request, "Incorrect password.")
        except PoliceStation.DoesNotExist:
            messages.error(request, "Station ID not found.")

    return render(request, 'police/login.html')


def police_dashboard(request):
    station_id = request.session.get('station_id')
    if not station_id:
        return redirect('police_login')

    try:
        station = PoliceStation.objects.get(station_id=station_id)
    except PoliceStation.DoesNotExist:
        return redirect('police_login')

    return render(request, 'police/dashboard.html', {'station': station})
