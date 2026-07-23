from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Default role is STUDENT; organizer accounts created via admin.
    """

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "role": {"read_only": True},
        }

    def create(self, validated_data):
        # Ensure new registrations default to STUDENT
        validated_data["role"] = User.Role.STUDENT
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    """
    Extends SimpleJWT's TokenObtainPairSerializer to include user details
    in the login response.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token payload
        token["username"] = user.username
        token["role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role": self.user.role,
        }

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving/updating the authenticated user's profile.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "username",
            "role",
            "date_joined",
        ]


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout.
    Validates and blacklists the provided refresh token.
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
        except TokenError:
            raise serializers.ValidationError(
                "Invalid or expired refresh token."
            )
