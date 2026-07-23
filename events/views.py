import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Event
from .serializers import EventSerializer
from .permissions import IsOrganizer, IsOwnerOrReadOnly


class EventFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(
        field_name="event_date",
        lookup_expr="date",
    )

    class Meta:
        model = Event
        fields = ["category", "date"]


class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = EventFilter
    search_fields = ["title", "description", "location"]
    ordering_fields = ["event_date", "created_at", "title"]
    ordering = ["event_date"]

    def get_queryset(self):
        queryset = Event.objects.select_related("organizer")
        user = self.request.user

        if not user.is_authenticated:
            return queryset.filter(status=Event.Status.PUBLISHED)

        if user.role == user.Role.ADMIN:
            return queryset

        if user.role == user.Role.ORGANIZER:
            return queryset.filter(
                Q(status=Event.Status.PUBLISHED) | Q(organizer=user)
            )

        return queryset.filter(status=Event.Status.PUBLISHED)


    def get_permissions(self):

        if self.request.method == "POST":
            return [IsOrganizer()]

        return [IsAuthenticatedOrReadOnly()]


    def perform_create(self, serializer):
        serializer.save(
            organizer=self.request.user
        )


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        queryset = Event.objects.select_related("organizer")
        user = self.request.user

        if not user.is_authenticated:
            return queryset.filter(status=Event.Status.PUBLISHED)

        if user.role == user.Role.ADMIN:
            return queryset

        if user.role == user.Role.ORGANIZER:
            return queryset.filter(
                Q(status=Event.Status.PUBLISHED) | Q(organizer=user)
            )

        return queryset.filter(status=Event.Status.PUBLISHED)
