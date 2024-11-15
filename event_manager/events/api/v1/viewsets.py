"""
Views for the V1 API.
"""
from rest_framework import viewsets, status

from event_manager.events.models import Event, Speaker, Category, Attendee, Reservation
from .serializers import EventSerializer, SpeakerSerializer, CategorySerializer, AttendeeSerializer, \
    ReservationSerializer

class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SpeakerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing speakers.
    """
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AttendeeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing attendees.
    """
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing reservation.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
