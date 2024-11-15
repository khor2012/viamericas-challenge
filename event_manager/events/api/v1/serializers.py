from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from event_manager.events.models import Event, Speaker, Category, Attendee, Reservation, EventCategory


class EventSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Event
        fields = ('title', 'date', 'location', 'description', 'capacity', 'categories',)

    def save(self, **kwargs):
        categories = self.validated_data.pop('categories')
        instance = super().save(**kwargs)
        instance.categories.all().delete()
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            EventCategory.objects.get_or_create(category=category, event=instance)
        instance.save()



class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
