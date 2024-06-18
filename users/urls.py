from rest_framework import routers

from .views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="users")

# include rest to modules urls
urlpatterns = []
urlpatterns += router.urls

# add a flag for
# handling the 404 error
handler404 = "prediction.views.error_404_view"
handler500 = "prediction.views.error_500_view"
