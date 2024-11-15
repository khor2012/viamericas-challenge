from django.contrib import admin
from event_manager.events.models import (
    Event,
    Attendee,
    Speaker,
    EventCategory,
    Reservation,
)


@admin.action(description="Cancel events.")
def make_cancel(modeladmin, request, queryset):
    queryset.update(status=Event.EventStatus.CANCELED)


class CategoryInline(admin.TabularInline):
    model = EventCategory


class SpeakerInline(admin.TabularInline):
    model = Event.speakers.through


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_filter = ["title", "categories__category", "location", "status"]
    list_display = ["title", "date", "status", "location", "capacity"]
    search_fields = ["title", "description", "location"]
    readonly_fields = [
        "speakers",
    ]
    inlines = [CategoryInline, SpeakerInline]

    actions = [make_cancel]


class AttendeeAdmin(admin.ModelAdmin):
    model = Attendee
    list_display = ["name", "phone", "email"]


class SpeakerAdmin(admin.ModelAdmin):
    model = Speaker
    list_display = ["name", "phone", "email"]


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ["event", "attendee", "created_at"]
    list_filter = [
        "event__title",
    ]
    search_fields = ["event__description", "attendee__name"]


admin.site.register(Event, EventAdmin)
admin.site.register(Attendee, AttendeeAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Reservation, ReservationAdmin)
