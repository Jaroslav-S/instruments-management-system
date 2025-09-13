from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extend JWT payload with custom user fields (e.g., role).
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # Assumes your User model has a field "role"
        token['role'] = getattr(user, 'role', 'read')  # default role = read

        return token