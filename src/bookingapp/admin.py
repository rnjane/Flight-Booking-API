from django.contrib import admin
from .models import Flight, FlightBooking, PassportPhoto

admin.site.register(Flight)
admin.site.register(FlightBooking)
admin.site.register(PassportPhoto)