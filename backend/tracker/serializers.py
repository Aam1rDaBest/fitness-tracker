from rest_framework_simplejwt_mongoengine.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer
from .authentication import MongoAuthBackend
from rest_framework import serializers

class CustomTokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def validate(self, attrs):
        # Perform the standard validation first
        data = super().validate(attrs)
        
        # Extract username and password from request data
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Authenticate the user
        user = MongoAuthBackend().authenticate(request=None, username=username, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        
        # Return the token data
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()