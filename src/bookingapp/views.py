from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, response, permissions, generics, views, authtoken
from rest_framework import serializers as sz
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework.decorators import permission_classes
from . import serializers, models


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
                        status=status.HTTP_404_NOT_FOUND)
        else:
            token, _ = authtoken.models.Token.objects.get_or_create(user=user)
            return response.Response({'token': token.key},
                    status=status.HTTP_200_OK)


class UploadPassport(generics.CreateAPIView):
    serializer_class = serializers.PassportSerializer
    queryset = models.PassportPhoto.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeletePassport(generics.DestroyAPIView):
    serializer_class = serializers.PassportSerializer
    queryset = models.PassportPhoto.objects.all()


class UpdatePassport(generics.UpdateAPIView):
    serializer_class = serializers.PassportSerializer
    queryset = models.PassportPhoto.objects.all()


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


class ViewBookings(generics.ListAPIView):
    serializer_class = serializers.FlightBookingSerializer
    queryset = models.FlightBooking.objects.all()


class CheckFlightStatus(generics.RetrieveAPIView):
    serializer_class = serializers.FlightBookingSerializer
    queryset = models.FlightBooking.objects.all()