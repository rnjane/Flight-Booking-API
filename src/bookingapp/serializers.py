from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class PassportSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    class Meta:
        model = models.PassportPhoto
        fields = ['owner', 'image', 'id']


class FlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flight
        fields = '__all__'


class FlightBookingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    flight = FlightsSerializer(read_only=True)
    class Meta:
        model = models.FlightBooking
        fields = ['owner', 'flight']