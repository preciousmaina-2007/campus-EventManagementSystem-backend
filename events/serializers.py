from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    organizer_name = serializers.CharField(
        source="organizer.username",
        read_only=True
    )

    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Event capacity must be at least one."
            )
        return value

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "event_date",
            "capacity",
            "category",
            "status",
            "organizer",
            "organizer_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "organizer",
            "created_at",
            "updated_at",
        ]
