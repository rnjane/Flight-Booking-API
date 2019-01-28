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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)