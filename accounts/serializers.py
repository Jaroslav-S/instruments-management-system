from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that adds a frontend role to the token response.
    Works with Django's default User model.
    """

    @classmethod
    def get_token(cls, user):
        # Generate the standard token
        token = super().get_token(user)

        # Map backend user attributes to frontend role
        if user.is_superuser:
            role = "admin"
        elif user.is_staff:
            role = "write"
        else:
            role = "read"

        # Optionally include role inside the JWT token itself
        token['role'] = role
        return token

    def validate(self, attrs):
        # Perform standard validation
        data = super().validate(attrs)

        # Add frontend role to the response JSON
        user = self.user
        if user.is_superuser:
            role = "admin"
        elif user.is_staff:
            role = "write"
        else:
            role = "read"

        data['role'] = role
        return data