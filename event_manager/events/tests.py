from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from event_manager.events.models import Event, Reservation, Attendee
from datetime import datetime
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class EventTestCase(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title="Event 1",
            description="Event 1",
            location="A location",
            capacity=1,
            date=datetime.now(),
        )

    def test_capacity(self):
        """Capacity limit works for reservation."""
        attendee_1 = Attendee.objects.create(name="attendee 1", email="1@email.com")
        attendee_2 = Attendee.objects.create(name="attendee 2", email="2@email.com")
        Reservation.objects.create(event=self.event, attendee=attendee_1)

        with self.assertRaises(ValidationError):
            Reservation.objects.create(event=self.event, attendee=attendee_2)


class APIClientTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password = "pass"
        self.user = User.objects.create_user(username="test", password=self.password)

    def authenticate(self):
        response = self.client.post(
            "/api/auth/token",
            {"username": "test", "password": self.password},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client = APIClient(
            headers={"Authorization": f"Token {response.json()["token"]}"}
        )

    def test_authorized(self):
        """No authenticated users get error."""
        self.authenticate()
        response = self.client.get("/api/v1/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized(self):
        """Not authenticated users get error."""
        response = self.client.get("/api/v1/events/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
