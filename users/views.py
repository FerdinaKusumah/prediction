from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from prediction.pagination import LargeResultsSetPagination
from prediction.permissions import (
    IsAdminUser,
)
from prediction.views import BaseViewSet
from users.serializer.token import (
    CustomTokenObtainPairSerializer,
    OauthTokenObtainPairSerializer,
)
from users.serializer.users import UserSerializer
from .models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class OauthGoogleTokenView(TokenObtainPairView):
    serializer_class = OauthTokenObtainPairSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """oauth google"""
        try:
            token = request.data.get("token", None)
            if not token:
                return Response(
                    {"error": "invalid token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Specify the CLIENT_ID of the app that accesses the backend:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), settings.OAUTH_GOOGLE_CLIENT_ID
            )

            user, _ = User.objects.update_or_create(
                username=".".join(id_info["name"].lower().split()),
                email=id_info["email"],
                first_name=id_info["given_name"],
                last_name=id_info["family_name"],
                is_staff=True,
                is_superuser=False,
            )

            # access token for that user
            access_token = AccessToken.for_user(user=user)
            # refresh token for that user
            refresh_token = RefreshToken.for_user(user=user)

            return Response(
                {"access": str(access_token), "refresh": str(refresh_token)},
                status=status.HTTP_200_OK,
            )
        except ValueError:
            # Invalid token
            pass

        return Response(
            {"error": "invalid token"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserViewSet(BaseViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    # only admin can access this users
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination
    queryset = User.objects.select_related()

    @action(detail=False, methods=["GET"], url_path="history", url_name="history")
    def history(self, request, *args, **kwargs):
        """List of records"""
        return super().history_module(User)

    @action(detail=False, methods=["GET"], url_path="me", url_name="me")
    def get_user_info(self, request, *args, **kwargs):
        """Get information about the current user."""
        serializer = UserSerializer(request.user)
        # return response
        return super().response_success(serializer.data)

    def list(self, request, *args, **kwargs):
        """List of records"""
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create new records"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return super().response_success(serializer.data)

        return super().response_bad_request(serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        """Detail records"""
        rec = User.objects.filter(pk=kwargs["pk"])
        if not rec.exists():
            return super().response_bad_request({"error": "record not found"})

        rec = rec.first()
        serializer = UserSerializer(rec)
        # return response
        return super().response_success(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update records"""
        rec = User.objects.filter(pk=kwargs["pk"])
        if not rec.exists():
            return super().response_bad_request({"error": "record not found"})

        rec = rec.first()
        serializer = UserSerializer(rec, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return super().response_success(serializer.data)

        return super().response_bad_request(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        """Delete records"""
        rec = User.objects.filter(pk=kwargs["pk"])
        if not rec.exists():
            return super().response_bad_request({"error": "record not found"})

        rec = rec.first()
        rec.delete()
        return super().response_no_content()
