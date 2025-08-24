# users/views.py

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserProfileSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView 


class UserRegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny] 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserProfileSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    """
    API endpoint for user login (obtains JWT access and refresh tokens).
    Uses djangorestframework_simplejwt's TokenObtainPairView.
    """
    permission_classes = [permissions.AllowAny] 


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] 
    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()