from rest_framework import routers

from .views import PredictViewSet

router = routers.SimpleRouter(trailing_slash=False)

# predict
router.register("predictions", PredictViewSet, basename="predict")

urlpatterns = []
urlpatterns += router.urls
