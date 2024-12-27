from django import forms
from .models import Station

class EnergoForm(forms.ModelForm):
    stations = Station.objects.all()
    ENERGO_CHOICE = [(station.id, station.name) for station in stations]
    selected = forms.ChoiceField(choices=ENERGO_CHOICE)