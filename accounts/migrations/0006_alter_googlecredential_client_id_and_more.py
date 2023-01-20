# Generated by Django 4.1.5 on 2023-01-20 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_googlecredential_client_secret_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlecredential',
            name='client_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='googlecredential',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='googlecredential',
            name='scopes',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='googlecredential',
            name='token',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]