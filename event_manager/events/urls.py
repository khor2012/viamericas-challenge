from django.urls import path, include

urlpatterns = [
    path("api/", include("event_manager.events.api.urls", namespace="event_api")),
]
