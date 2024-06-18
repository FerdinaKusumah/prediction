"""
URL configuration for song project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users.views import CustomTokenObtainPairView, OauthGoogleTokenView

schema_view = get_schema_view(
    openapi.Info(
        title="Predictions API",
        default_version="v1",
        description="Predictions API",
        contact=openapi.Contact(email="admin@devdat.ai"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("users/", include("users.urls")),
    path("predict/", include("predict.urls")),
    # jwt urls and oauth google token
    path("api/oauth/google", OauthGoogleTokenView.as_view(), name="oauth_google"),
    path("api/token", CustomTokenObtainPairView.as_view(), name="token_request"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # swagger documentation
    path(
        "swagger<format>", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# add a flag for
# handling the 404 error
handler404 = "prediction.views.error_404_view"
handler500 = "prediction.views.error_500_view"
