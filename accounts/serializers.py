from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationSerializer(serializers.ModelSerializer): 
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
    "password": {"write_only": True}
}    
        
def create(self, validated_data):
    return User.objects.create_user(**validated_data)        

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
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