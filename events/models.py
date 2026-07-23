from django.db import models
from django.conf import settings


class Event(models.Model):

    class Category(models.TextChoices):
        WORKSHOP = "WORKSHOP", "Workshop"
        SEMINAR = "SEMINAR", "Seminar"
        HACKATHON = "HACKATHON", "Hackathon"
        SPORTS = "SPORTS", "Sports"
        SOCIAL = "SOCIAL", "Social"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        CANCELLED = "CANCELLED", "Cancelled"

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    event_date = models.DateTimeField()
    capacity = models.PositiveIntegerField()

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.WORKSHOP,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['event_date']


    def __str__(self):
        return self.title