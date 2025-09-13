from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Overridden JWT endpoint that returns not only access and refresh tokens
    but also the user's role.
    """
    serializer_class = CustomTokenObtainPairSerializer