from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, response, permissions, generics, views, authtoken
from rest_framework import serializers as sz
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.decorators import permission_classes
from django.shortcuts import render, reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from . import serializers, models

from rest_framework.decorators import permission_classes
from .serializers import UserSerializer

User = get_user_model()

class UserCreate(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()


class LoginUser(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return response.Response({'error': 'Please provvide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return response.Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_401_UNAUTHORIZED)
        else:
            token, _ = authtoken.models.Token.objects.get_or_create(user=user)
            return response.Response({'token': token.key},
                    status=status.HTTP_200_OK)


class UploadPassport(generics.CreateAPIView):
    serializer_class = serializers.PassportSerializer
    queryset = models.PassportPhoto.objects.all()

    def perform_create(self, serializer):
        try:
            photo = models.PassportPhoto.objects.get(owner=self.request.user)
            photo.delete()
            serializer.save(owner=self.request.user)
        except ObjectDoesNotExist:
            serializer.save(owner=self.request.user)


class DeletePassport(generics.DestroyAPIView):
    serializer_class = serializers.PassportSerializer

    def get_object(self):
        return models.PassportPhoto.objects.get(owner=self.request.user)

class UpdatePassport(generics.UpdateAPIView):
    serializer_class = serializers.PassportSerializer
    
    def get_object(self):
        return models.PassportPhoto.objects.get(owner=self.request.user)


class ViewFlights(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.FlightsSerializer
    queryset = models.Flight.objects.all()


class CreateBooking(generics.CreateAPIView):
    serializer_class = serializers.FlightBookingSerializer
    queryset = models.FlightBooking.objects.all()

    def perform_create(self, serializer):
        try:
            flight = models.Flight.objects.get(name=self.kwargs['flight_name'])
        except ObjectDoesNotExist:
            raise sz.ValidationError("The specified flight does not exist.")
        queryset = models.FlightBooking.objects.filter(owner=self.request.user, flight=self.kwargs['flight_name'])
        if queryset.exists():
            raise sz.ValidationError("You have already booked this flight.")
        serializer.save(flight_id=self.kwargs['flight_name'], owner=self.request.user)
        flight = models.FlightBooking.objects.get(flight_id=self.kwargs['flight_name'], owner=self.request.user)
        send_mail(
            'You have succesfully booked a flight',
            flight.flight.name + "Will be on " + flight.flight.date_time_of_flight.strftime("%Y-%m-%d %H:%M:%S"),
            settings.EMAIL_HOST_USER,
            [flight.owner.email],
            fail_silently=False,
        )


class ViewBookings(generics.ListAPIView):
    serializer_class = serializers.FlightBookingSerializer
    queryset = models.FlightBooking.objects.all()


class CheckFlightStatus(generics.RetrieveAPIView):
    serializer_class = serializers.FlightBookingSerializer
    queryset = models.FlightBooking.objects.all()


class FlightsReport(generics.ListAPIView):
    serializer_class = serializers.FlightBookingSerializer
    def get_queryset(self):
        time_threshold = datetime.now() - timedelta(hours=24)
        return models.FlightBooking.objects.filter(date_created__gte=time_threshold)


@permission_classes((IsAuthenticated, ))
def pay(request, pk):
    flight = models.Flight.objects.get(pk=pk)
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": flight.cost,
        "item_name": flight.name,
        "invoice": flight.name + request.user.username + flight.name,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('done', kwargs={"flight_name": flight.name})),
        "cancel_return": request.build_absolute_uri(reverse('canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "amount": flight.cost, "item_name": flight.name}
    return render(request, "payment.html", context)

@csrf_exempt
@permission_classes((IsAuthenticated, ))
def payment_done(request, flight_name):
    flight = models.Flight.objects.get(pk=flight_name)
    obj, created = models.FlightBooking.objects.get_or_create(
        owner=request.user,
        flight=flight,
        reserved=True
    )
    if obj:
        obj.reserved = True
        obj.save()

    context = {"amount": flight.cost, "item_name": flight.name}
    return render(request, 'done.html', context)


@csrf_exempt
@permission_classes((IsAuthenticated, ))
def payment_canceled(request):
    return render(request, 'cancelled.html')