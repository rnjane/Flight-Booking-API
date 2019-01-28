from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, response, permissions, generics, views, authtoken
from . import serializers, models
from rest_framework.decorators import permission_classes

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