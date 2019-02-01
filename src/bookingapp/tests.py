from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from model_mommy import mommy
import tempfile
from PIL import Image
from . import models, serializers

class TestsSetUp(APITestCase):
    fixtures = ['fixtures']
    def get_temporary_image(self):
        '''create a temporary image for testing purposes'''
        image = Image.new('RGB', (200, 200))
        temporary_image = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(temporary_image, 'jpeg')
        temporary_image.seek(0)
        return temporary_image

    def setUp(self):
        self.client = APIClient()
        User.objects.create_user(username='testuser', email='test@test.com', password='testpass12')
        test_user = User.objects.create_user(username='testuser1', email='test1@test.com', password='testpass12')
        self.user = User.objects.get(username='testuser1')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.post(reverse('upload_passport'), {'image': self.get_temporary_image()}, format='multipart')
        self.client.post(reverse('create_booking', kwargs={'flight_name': 'KQAB21361'}))


class UserAuthTests(TestsSetUp):
    '''Authentication related tests'''
    def test_user_login_successful_with_valid_credentials(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass12'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_with_wrong_credentials_fail(self):
        response = self.client.post(reverse('login'), {'username': 'wrongusername', 'password': 'wrongone'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_with_missing_credentials_fail(self):
        response = self.client.post(reverse('login'), {'password': 'wrongone'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fails_with_wrong_email(self):
        response = self.client.post(reverse('register'), {'username': 'test_user', 'email': 'testtest.com', 'password': 'testpass'})
        self.assertIn('Enter a valid email address.', response.data['email'])

    def test_user_register_fails_with_invalid_password(self):
        response = self.client.post(reverse('register'), {'username': 'test_user', 'email': 'test@test.com', 'password': 'short'})
        self.assertIn('Enter a valid password. Password should be at least 8 characters long.', response.data)


class FlightsTests(TestsSetUp):
    '''tests related to flights'''
    def test_user_can_view_all_flights(self):
        response = self.client.get(reverse('view_flights'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_create_a_booking(self):
        response = self.client.post(reverse('create_booking', kwargs={'flight_name': 'KQAB2136'}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_creating_a_booking_requires_login(self):
        unauthorized_client = APIClient()
        response = unauthorized_client.post(reverse('create_booking', kwargs={'flight_name': 'KQAB2135'}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_a_booking_fails_with_invalid_flight(self):
        response = self.client.post(reverse('create_booking', kwargs={'flight_name': 'NOEXIST'}))
        self.assertIn('The specified flight does not exist.', response.data)

    def test_user_cann_book_a_flight_twice(self):
        response = self.client.post(reverse('create_booking', kwargs={'flight_name': 'KQAB21361'}))
        self.assertIn('You have already booked this flight.', response.data)

    def test_user_can_view_their_bookings(self):
        response = self.client.get(reverse('view_bookings'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewing_bookings_requires_login(self):
        unauthorized_client = APIClient()
        response = unauthorized_client.get(reverse('view_bookings'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PassportsTests(TestsSetUp):
    '''Passports related tests'''
    def get_temporary_image(self):
        '''create a temporary image for testing purposes'''
        image = Image.new('RGB', (200, 200))
        temporary_image = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(temporary_image, 'jpeg')
        temporary_image.seek(0)
        return temporary_image

    def test_user_can_upload_a_passport(self):
        response = self.client.post(reverse('upload_passport'), {'image': self.get_temporary_image()}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_can_update_a_passport(self):
        response = self.client.put(reverse('update_passport'), {'image': self.get_temporary_image()}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_delete_a_passport(self):
        response = self.client.delete(reverse('remove_passport'), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
