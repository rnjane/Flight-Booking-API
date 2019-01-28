from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PassportPhoto(models.Model):
    owner = models.ForeignKey(User, related_name='passport', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(PassportPhoto, self).delete(*args, **kwargs)
        storage.delete(path)

class Flight(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    destination = models.CharField(max_length=30)
    capacity = models.IntegerField()
    departure_from = models.CharField(max_length=30)
    date_time_of_flight = models.DateTimeField()
    cost = models.FloatField(default=0.00)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date_time_of_flight']

class FlightBooking(models.Model):
    flight = models.OneToOneField(Flight, related_name='user_booking', on_delete=models.CASCADE, primary_key=True)
    owner = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False)