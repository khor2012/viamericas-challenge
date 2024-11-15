from django.test import TestCase

from django.test import Client
from rest_framework import status

from event_manager.events.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()


class EventsAPIV1TestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="test", password="pass")
        self.client.force_login(self.user)

    def test_create(self):
        """API stores an event after saving it."""
        response = self.client.post(
            "/api/v1/events/",
            {
                "title": "Test Event",
                "description": "Test Event",
                "date": "2020-01-10",
                "capacity": 2,
                "location": "Test Location",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Event.objects.get(title="Test Event")

    def test_create_with_categories(self):
        """API stores events with categories and creates them."""
        categories = ["demo", "example", "test"]

        response = self.client.post(
            "/api/v1/events/",
            {
                "title": "Test Event",
                "description": "Test Event",
                "date": "2020-01-10",
                "capacity": 2,
                "location": "Test Location",
                "categories": categories,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        event = Event.objects.get(title="Test Event")
        for category in event.categories.all():
            self.assertIn(category.name, categories)

    def test_search(self):
        """API allows searching events based on title."""
        categories = ["demo", "example", "test"]

        response = self.client.post(
            "/api/v1/events/",
            {
                "title": "Test Event",
                "description": "Test Event",
                "date": "2020-01-10",
                "capacity": 2,
                "location": "Test Location",
                "categories": categories,
            },
        )

        response = self.client.get("/api/v1/events/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 1)
        response = self.client.get("/api/v1/events/?search=hi")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["count"], 0)

    def test_delete(self):
        """API allows searching events based on title."""
        categories = ["demo", "example", "test"]

        response = self.client.post(
            "/api/v1/events/",
            {
                "title": "Test Event",
                "description": "Test Event",
                "date": "2020-01-10",
                "capacity": 2,
                "location": "Test Location",
                "categories": categories,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete("/api/v1/events/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        """API allows updating an event."""
        categories = ["demo", "example", "test"]
        response = self.client.post(
            "/api/v1/events/",
            {
                "title": "Test Event",
                "description": "Test Event",
                "date": "2020-01-10",
                "capacity": 2,
                "location": "Test Location",
                "categories": categories,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.patch(
            "/api/v1/events/1/",
            {"title": "Updated Title"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        event = Event.objects.get(id=1)
        self.assertEqual(event.title, "Updated Title")
