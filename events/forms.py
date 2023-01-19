from django import forms

from .models import Calendar, Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            'calendar', 'summary', 'location', 'description', 'start', 'end'
        ]
        widgets = {
            'calendar': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }
