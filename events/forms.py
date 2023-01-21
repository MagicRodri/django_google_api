from django import forms

from .models import Calendar, Event


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
            forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end':
            forms.DateTimeInput(attrs={'class': 'form-control'}),
        }
