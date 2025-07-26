
from django.shortcuts import render, redirect
from .models import FireStation
from django.contrib import messages
from .forms import FireStationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
def fire_login_view(request):
    if request.method == 'POST':
        station_id = request.POST.get('station_id')
        password = request.POST.get('password')

        try:
            station = FireStation.objects.get(station_id=station_id)
            if station.password == password:
                request.session['fire_station_id'] = station.station_id
                request.session['fire_station_name'] = station.name
                return redirect('fire_dashboard')
            else:
                messages.error(request, "Incorrect password.")
        except FireStation.DoesNotExist:
            messages.error(request, "Station ID not found.")

    return render(request, 'fire/login.html')

def fire_dashboard(request):
    station_id = request.session.get('fire_station_id')
    if not station_id:
        return redirect('fire_login')

    try:
        station = FireStation.objects.get(station_id=station_id)
    except FireStation.DoesNotExist:
        return redirect('fire_login')

    return render(request, 'fire/dashboard.html', {'station': station})

def fire_change_password(request):
    station_id = request.session.get('fire_station_id')
    if not station_id:
        return redirect('fire_login')

    station = FireStation.objects.get(station_id=station_id)

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
            return redirect('fire_dashboard')

    return render(request, 'fire/change_password.html', {'station': station})
