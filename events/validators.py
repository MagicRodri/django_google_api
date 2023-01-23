from django.core.exceptions import ValidationError

from .models import default_end, default_start


def clean_event_data(data):
    start = data.pop('start', None)
    end = data.pop('end', None)
    # Assign default values if user leaves empty
    data['start'] = start if start else default_start()
    data['end'] = end if end else default_end()
    # if data['start'] > data['end']:
    #     raise ValidationError('End must occur after start')
    return data