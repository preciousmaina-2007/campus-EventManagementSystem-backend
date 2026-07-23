from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Event


class EventAPITests(APITestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            username="organizer",
            password="secure-password-123",
            role=User.Role.ORGANIZER,
        )
        self.other_organizer = User.objects.create_user(
            username="other-organizer",
            password="secure-password-123",
            role=User.Role.ORGANIZER,
        )
        self.student = User.objects.create_user(
            username="student",
            password="secure-password-123",
        )
        self.admin_user = User.objects.create_user(
            username="admin",
            password="secure-password-123",
            role=User.Role.ADMIN,
        )
        self.published_event = self.create_event(
            title="Published workshop",
            status=Event.Status.PUBLISHED,
        )
        self.draft_event = self.create_event(
            title="Private draft",
            status=Event.Status.DRAFT,
        )

    def create_event(self, **overrides):
        defaults = {
            "title": "Campus workshop",
            "description": "Learn Django REST Framework.",
            "location": "Engineering Hall",
            "event_date": timezone.now() + timedelta(days=7),
            "capacity": 50,
            "category": Event.Category.WORKSHOP,
            "organizer": self.organizer,
        }
        defaults.update(overrides)
        return Event.objects.create(**defaults)

    def test_public_list_shows_only_published_events(self):
        response = self.client.get(reverse("event-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.published_event.id)

    def test_student_cannot_create_event(self):
        self.client.force_authenticate(self.student)

        response = self.client.post(
            reverse("event-list"),
            {
                "title": "Student event",
                "description": "Not permitted.",
                "location": "Library",
                "event_date": (timezone.now() + timedelta(days=3)).isoformat(),
                "capacity": 25,
                "category": Event.Category.SEMINAR,
                "status": Event.Status.DRAFT,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_organizer_can_create_event_and_becomes_owner(self):
        self.client.force_authenticate(self.organizer)

        response = self.client.post(
            reverse("event-list"),
            {
                "title": "Organizer event",
                "description": "An organizer-created event.",
                "location": "Auditorium",
                "event_date": (timezone.now() + timedelta(days=3)).isoformat(),
                "capacity": 25,
                "category": Event.Category.SEMINAR,
                "status": Event.Status.DRAFT,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["organizer"], self.organizer.id)

    def test_only_owner_or_admin_can_update_event(self):
        url = reverse("event-detail", args=[self.draft_event.id])
        self.client.force_authenticate(self.other_organizer)

        response = self.client.patch(url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(self.admin_user)
        response = self.client.patch(url, {"title": "Admin changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_event_list_filters_by_category_and_date(self):
        response = self.client.get(
            reverse("event-list"),
            {
                "category": Event.Category.WORKSHOP,
                "date": self.published_event.event_date.date().isoformat(),
                "search": "Published",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

# Create your tests here.
