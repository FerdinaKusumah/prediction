from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token["email"] = user.email
        return token


class OauthTokenObtainPairSerializer(serializers.Serializer):
    token = serializers.CharField()
