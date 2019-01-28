# Generated by Django 2.1.5 on 2019-01-28 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookingapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('destination', models.CharField(max_length=30)),
                ('capacity', models.IntegerField()),
                ('departure_from', models.CharField(max_length=30)),
                ('date_time_of_flight', models.DateTimeField()),
                ('cost', models.FloatField(default=0.0)),
            ],
            options={
                'ordering': ['date_time_of_flight'],
            },
        ),
        migrations.CreateModel(
            name='FlightBooking',
            fields=[
                ('flight', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_booking', serialize=False, to='bookingapp.Flight')),
                ('reserved', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
