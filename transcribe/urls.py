from django.urls import path
from .views import TranscribeSetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transcribe-set', TranscribeSetViewSet, basename='transcribe-set')

urlpatterns = router.urls