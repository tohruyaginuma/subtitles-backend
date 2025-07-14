from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import CustomTokenRefreshSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({
                    "data": {"user_id": user.id},
                    "error": None
                }, status=status.HTTP_201_CREATED)

            return Response({
                "data": None,
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "data": None,
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response(
                {"data": serializer.validated_data, "error": None},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"data": None, "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response(
                {"data": serializer.validated_data, "error": None},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"data": None, "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )