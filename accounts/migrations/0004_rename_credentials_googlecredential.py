# Generated by Django 4.1.5 on 2023-01-19 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_credentials'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Credentials',
            new_name='GoogleCredential',
        ),
    ]