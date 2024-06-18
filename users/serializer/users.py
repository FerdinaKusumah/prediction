from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField()
    email = serializers.EmailField()
    is_staff = serializers.BooleanField(default=True)
    is_active = serializers.BooleanField(default=True)
    date_joined = serializers.DateTimeField(required=False)

    class Meta:
        model = User
        extra_kwargs = {"password": {"write_only": True}}
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "date_joined",
            "is_active",
        ]
