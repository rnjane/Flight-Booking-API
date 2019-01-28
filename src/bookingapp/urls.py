from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from . import views

urlpatterns = [
    #User Auth URLs
    path('api-auth/', include('rest_framework.urls')),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.UserCreate.as_view(), name='register'),   

    #Passport operations
    path('upload-passport/', views.UploadPassport.as_view(), name='upload_passport'),
    path('remove-passport/<int:pk>/', views.DeletePassport.as_view(), name='remove_passport'),
    path('update-passport/<int:pk>/', views.UpdatePassport.as_view(), name='update_passport'),

    #flight booking operations
    path('flights/', views.ViewFlights.as_view(), name='view_flights'),
    path('create-booking/<str:flight_name>/', views.CreateBooking.as_view(), name='create_booking'),
    path('bookings/', views.ViewBookings.as_view(), name='view_bookings'),
    path('check-status/<str:pk>/', views.CheckFlightStatus.as_view(), name='check_flight_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)