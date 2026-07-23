from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    organizer_name = serializers.CharField(
        source="organizer.username",
        read_only=True
    )

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