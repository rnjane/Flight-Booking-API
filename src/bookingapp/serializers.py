from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models
from rest_framework.exceptions import ValidationError
import re

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password": {"write_only": True}}
            

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Enter a valid email address.")
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            raise ValidationError("Enter a valid password. Password should be at least 8 characters long.")
        user = User(username=username, email=email)
        user.set_password(password)
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
        fields = ['owner', 'flight', 'reserved']