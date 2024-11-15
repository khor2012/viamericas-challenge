from rest_framework.serializers import ValidationError
from django.db import models


class Category(models.Model):
    """
    A model representing an event category.
    """

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class Speaker(models.Model):
    """
    A model representing a speaker.
    """

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "email")


class Event(models.Model):
    """
    A model representing an event.
    """

    class EventStatus(models.TextChoices):
        """
        Available statuses for an event
        """

        IN_PROGRESS = "in_progress"
        CANCELED = "canceled"

    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    status = models.CharField(
        max_length=30, choices=EventStatus.choices, default=EventStatus.IN_PROGRESS
    )
    speakers = models.ManyToManyField(Speaker, related_name="speakers")
    categories = models.ManyToManyField(Category, related_name="categories")

    def get_attendees(self):
        """
        Returns a list of all attendees. Attendee that have a reservation for this event.
        """
        return Attendee.objects.filter(
            id__in=Reservation.objects.filter(event=self).values_list(
                "attendee", flat=True
            )
        )

    def __str__(self):
        return f"{self.title} - {self.date}"

    class Meta:
        ordering = ["date"]


class Attendee(models.Model):
    """
    A model representing an attendee.
    """

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ["name"]
        unique_together = ("name", "email")


class Reservation(models.Model):
    """
    A model representing a reservation in an event.
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} - {self.attendee.name}"

    class Meta:
        ordering = ["event"]
        unique_together = ("event", "attendee")

    def save(self, *args, **kwargs):
        if self.event.capacity <= Reservation.objects.filter(event=self.event).count():
            raise ValidationError("Reservation is already full")
        super().save(*args, **kwargs)
