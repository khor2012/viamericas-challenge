from rest_framework import serializers

from event_manager.events.models import (
    Event,
    Speaker,
    Category,
    Attendee,
    Reservation,
)


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            self.fail("invalid")


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, read_only=True)
    categories = CustomSlugRelatedField(
        many=True, slug_field="name", queryset=Category.objects.all()
    )

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
        categories = self.validated_data.pop("categories", [])
        instance = super().save(**kwargs)
        if categories:
            instance.categories.all().delete()
            for category in categories:
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
