from rest_framework import serializers

from event_manager.events.models import (
    Event,
    Speaker,
    Category,
    Attendee,
    Reservation,
)


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Category.objects.all()
    )
    speakers = SpeakerSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            "title",
            "date",
            "location",
            "description",
            "capacity",
            "status",
            "categories",
            "speakers",
        )

    def save(self, **kwargs):
        categories = self.validated_data.pop("categories")
        instance = super().save(**kwargs)
        instance.categories.all().delete()
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            instance.categories.add(category)
        instance.save()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
