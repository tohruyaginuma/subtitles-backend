from django.urls import path
from .views import live

urlpatterns = [
    path("live/", live, name="health-live"),
]