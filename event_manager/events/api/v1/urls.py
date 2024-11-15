from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .viewsets import EventViewSet, AttendeeViewSet, CategoryViewSet, ReservationViewSet, SpeakerViewSet

app_name = 'v1_api'

router = SimpleRouter()
router.register('events', EventViewSet)
router.register('attendees', AttendeeViewSet)
router.register('categories', CategoryViewSet)
router.register('reservations', ReservationViewSet)
router.register('speakers', SpeakerViewSet)

urlpatterns = [

]

urlpatterns += router.urls
