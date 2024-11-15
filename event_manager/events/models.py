from rest_framework.serializers import ValidationError
from django.db import models

class Event(models.Model):
    """
    A model representing an event.
    """
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()

    def get_attendees(self):
        """
        Returns a list of all attendees. Attendee that have a reservation for this event.
        """
        return Attendee.objects.filter(id__in=Reservation.objects.filter(event=self).values_list('attendee', flat=True))

    def __str__(self):
        return f'{self.title} - {self.date}'

    class Meta:
        ordering = ['date']


class Speaker(models.Model):
    """
    A model representing a speaker.
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'email')


class Attendee(models.Model):
    """
    A model representing an attendee.
    """
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        ordering = ['name']
        unique_together = ('name', 'email')


class EventSpeaker(models.Model):
    """
    A model representing an event speaker.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event.title} - {self.speaker.name}'

    class Meta:
        ordering = ['event']
        unique_together = ('event', 'speaker')


class Reservation(models.Model):
    """
    A model representing a reservation in an event.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.event.title} - {self.attendee.name}'

    class Meta:
        ordering = ['event']
        unique_together = ('event', 'attendee')

    def save(self, *args, **kwargs):
        if self.event.capacity <= Reservation.objects.filter(event=self.event).count():
            raise ValidationError('Reservation is already full')
        super().save(*args, **kwargs)

class Category(models.Model):
    """
    A model representing an event category.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']


class EventCategory(models.Model):
    """
    A model representing an event category.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f'{self.event.title} - {self.category.name}'

    @property
    def name(self):
        return self.category.name

    class Meta:
        ordering = ['event']
        unique_together = ('event', 'category')
