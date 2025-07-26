from django import forms
from .models import  FireStation

POSTAL_CHOICES = [
    ('5174', 'Ramna'),
    ('1126', 'Dhanmondi'),
    ('9373', 'Shahbag'),
    ('7312', 'New Market'),
    ('3134', 'Lalbagh'),
    ('1337', 'Kotwali'),
    ('3456', 'Hazaribagh'),
    ('6785', 'Kamrangirchar'),
]
class FireStationForm(forms.ModelForm):
    postal_code = forms.ChoiceField(choices=POSTAL_CHOICES)

    class Meta:
        model = FireStation
        fields = ['station_id', 'name', 'postal_code']
        labels = {'name': 'Station Name'}

    def clean_station_id(self):
        station_id = self.cleaned_data['station_id']
        if FireStation.objects.filter(station_id=station_id).exists():
            raise forms.ValidationError("🚫 A fire station with this ID already exists.")
        return station_id
