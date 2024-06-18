from auditlog.registry import auditlog
from django.conf import settings
from django.db import models


class Prediction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="predictions"
    )
    input_image = models.ImageField(upload_to="predictions/images")
    predicted_label = models.CharField(max_length=255, null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Prediction {self.id} by {self.user}"


# audit all activity
auditlog.register(Prediction)
