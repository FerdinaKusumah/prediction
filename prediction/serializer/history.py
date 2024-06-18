from auditlog.models import LogEntry
from rest_framework import serializers

from users.models import User


class NestedUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class HistoryModelSerializer(serializers.ModelSerializer):
    record_id = serializers.CharField(source="object_id")
    record_pk = serializers.CharField(source="object_pk")
    record_name = serializers.CharField(source="object_repr")
    action = serializers.CharField(source="get_action_display")

    # nested fields
    actor = NestedUserModelSerializer()
    changes = serializers.SerializerMethodField()

    @staticmethod
    def get_changes(obj):
        return obj.changes

    class Meta:
        model = LogEntry
        fields = [
            "id",
            "record_id",
            "record_pk",
            "record_name",
            "action",
            "timestamp",
            # nested fields
            "actor",
            "changes",
        ]
