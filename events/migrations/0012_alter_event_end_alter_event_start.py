# Generated by Django 4.1.5 on 2023-01-20 18:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_event_event_id_alter_event_end_alter_event_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 22, 18, 23, 49, 492477)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 21, 18, 23, 49, 492460)),
        ),
    ]
