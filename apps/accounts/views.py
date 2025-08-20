from rest_framework.views import APIView
from .serializers import RegisterSerializer, MeSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from apps.common.responses import created, ok
from apps.accounts.models import User

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return created()

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ok(serializer.validated_data)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return ok(serializer.validated_data)

class MeView(APIView):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = MeSerializer(user)
        return ok(serializer.data)