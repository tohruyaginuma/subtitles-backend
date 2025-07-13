from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny

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

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try: 
            serializer = LoginSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.validated_data["user"]
                refresh = RefreshToken.for_user(user)
                return Response({
                    "data": {
                        "refresh_token": str(refresh),
                        "access_token": str(refresh.access_token),
                        "email": user.email,
                    },
                    "error": None
                }, status=status.HTTP_200_OK)
            return Response({
                "data": None,
                "error": serializer.errors
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({
                "data": None,
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)