from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Event
from .serializers import EventSerializer
from .permissions import IsOrganizer, IsOwnerOrReadOnly


class EventListCreateView(generics.ListCreateAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer


    def get_permissions(self):

        if self.request.method == "POST":
            return [IsOrganizer()]

        return [IsAuthenticatedOrReadOnly()]


    def perform_create(self, serializer):
        serializer.save(
            organizer=self.request.user
        )


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [
        IsOwnerOrReadOnly
    ]