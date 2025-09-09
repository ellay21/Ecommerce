from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register

class UserDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve the details of the currently authenticated user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can access

    def get_object(self):
        # This view returns the user associated with the request
        return self.request.user
