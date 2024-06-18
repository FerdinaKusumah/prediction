from rest_framework import serializers

from predict.models import Prediction
from users.serializer.users import UserSerializer


class PredictionSerializer(serializers.ModelSerializer):
    predicted_label = serializers.CharField(read_only=True)
    metadata = serializers.JSONField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    # nested serializer
    user = UserSerializer(read_only=True)

    class Meta:
        model = Prediction
        fields = [
            "id",
            "user_id",
            "input_image",
            "predicted_label",
            "metadata",
            "created_at",
            # nested
            "user",
        ]
