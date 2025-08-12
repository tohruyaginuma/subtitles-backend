from django.urls import path
from .views import live, ready

urlpatterns = [
    path("live/", live, name="health-live"),
    path("ready/", ready),
]