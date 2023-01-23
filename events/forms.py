from django import forms

from .models import Calendar, Event, default_end, default_start
from .validators import clean_event_data


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['calendar'].queryset = Calendar.objects.filter(user=user)

    class Meta:
        model = Event
        fields = [
            'calendar', 'summary', 'location', 'description', 'start', 'end'
        ]
        widgets = {
            'calendar':
            forms.Select(attrs={'class': 'form-control'}),
            'summary':
            forms.TextInput(attrs={'class': 'form-control'}),
            'location':
            forms.TextInput(attrs={'class': 'form-control'}),
            'description':
            forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 40,
                'rows': 4
            }),
            'start':
            forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': default_start().strftime(
                        '%Y-%m-%d %H:%M:%S')
                }),
            'end':
            forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': default_end().strftime('%Y-%m-%d %H:%M:%S')
                }),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        return clean_event_data(cleaned_data)