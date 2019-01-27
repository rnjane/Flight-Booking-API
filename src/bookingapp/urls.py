from django.urls import path
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.UserCreate.as_view(), name='register'),   
]