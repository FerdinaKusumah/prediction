import numpy as np
import tensorflow as tf
from django.conf import settings
from rest_framework.decorators import action

from predict.serializer.prediction import PredictionSerializer
from prediction.pagination import LargeResultsSetPagination
from prediction.permissions import (
    IsAuthenticatedUser,
)
from prediction.views import BaseViewSet
from .models import Prediction


class PredictViewSet(BaseViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    # only user that authenticated can access this source
    permission_classes = [IsAuthenticatedUser]
    serializer_class = PredictionSerializer
    pagination_class = LargeResultsSetPagination
    queryset = Prediction.objects.select_related()

    @action(detail=False, methods=["GET"], url_path="history", url_name="history")
    def history(self, request, *args, **kwargs):
        """List of records"""
        return super().history_module(Prediction)

    @staticmethod
    def predict_image(file_path: str) -> int:
        try:
            img = tf.keras.utils.load_img(file_path, target_size=(150, 150))

            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)  # Create a batch
            predictions = settings.BASE_MODEL.predict(img_array)
            return int(np.argmax(predictions))
        except Exception:
            return -1

    def list(self, request, *args, **kwargs):
        """List of records"""
        return super(PredictViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create new records"""
        file_obj = request.data.get("input_image", None)
        if not file_obj:
            return super().response_bad_request({"error": "input_image is required"})

        if not file_obj.name.lower().endswith((".jpg", ".jpeg", ".png")):
            return super().response_bad_request(
                {"error": "Only JPG and PNG files are allowed"}
            )

        # save to database
        resp = Prediction.objects.create(
            user_id=request.user.id,
            input_image=request.data["input_image"],
        )

        # get predictions
        prediction = self.predict_image(resp.input_image.path)
        if prediction == -1:
            return super().response_bad_request(
                {"error": "cannot create prediction, please check images"}
            )

        # label prediction
        label = settings.PLANT_DISEASE_MAP[prediction]
        resp.predicted_label = label
        resp.metadata = {
            "prediction": prediction,
            "label": label,
            "file_name": resp.input_image.name,
        }
        resp.save()

        serializer = PredictionSerializer(resp)
        return super().response_success(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Detail records"""
        rec = Prediction.objects.filter(pk=kwargs["pk"])
        if not rec.exists():
            return super().response_bad_request({"error": "record not found"})

        rec = rec.first()
        serializer = PredictionSerializer(rec)
        # return response
        return super().response_success(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update records"""
        file_obj = request.data.get("input_image", None)
        if not file_obj:
            return super().response_bad_request({"error": "input_image is required"})

        if not file_obj.name.lower().endswith((".jpg", ".jpeg", ".png")):
            return super().response_bad_request(
                {"error": "Only JPG and PNG files are allowed"}
            )

        rec = Prediction.objects.filter(pk=kwargs["pk"])
        if not rec.exists():
            return super().response_bad_request({"error": "record not found"})

        rec = rec.first()
        serializer = PredictionSerializer(rec, data=request.data)
        if serializer.is_valid():
            if "input_image" in request.FILES:
                rec.input_image.delete()
                rec.input_image = request.FILES["input_image"]

            serializer.save()

            # get predictions
            prediction = self.predict_image(rec.input_image.path)
            if prediction == -1:
                return super().response_bad_request(
                    {"error": "cannot create prediction, please check images"}
                )

            # label prediction
            label = settings.PLANT_DISEASE_MAP[prediction]
            rec.predicted_label = label
            rec.metadata |= {
                "prediction": prediction,
                "label": label,
                "file_name": rec.input_image.name,
            }
            rec.save()
            return super().response_success(serializer.data)

        return super().response_bad_request(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        """Delete records"""
        rec = Prediction.objects.filter(pk=kwargs["pk"])
        if not rec.exists():
            return super().response_bad_request({"error": "record not found"})

        rec = rec.first()
        # delete images from storage
        rec.input_image.delete()
        # delete actual records
        rec.delete()
        return super().response_no_content()
