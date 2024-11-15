"""
Views for the V1 API.
"""

from rest_framework import viewsets

from event_manager.events.models import Event, Speaker, Category, Attendee, Reservation
from .serializers import (
    EventSerializer,
    SpeakerSerializer,
    CategorySerializer,
    AttendeeSerializer,
    ReservationSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing events.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ("title", "categories__name", "location")
    search_fields = ("title", "description", "location")


class SpeakerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing speakers.
    """

    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    search_fields = ("name", "phone", "email")


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ("name",)


class AttendeeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing attendees.
    """

    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    search_fields = ("name", "phone", "email")


class ReservationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing reservation.
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
