from django.urls import path
from .views import TranscribeSetViewSet

urlpatterns = [
    path('transcribe-set/', TranscribeSetViewSet.as_view({'get': 'list'})),
    path('transcribe-set/<int:pk>/', TranscribeSetViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
]