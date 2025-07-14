from django.urls import path
from .views import HistorySetViewSet

urlpatterns = [
    path('history-set/', HistorySetViewSet.as_view({'get': 'list'})),
    path('history-set/<int:pk>/', HistorySetViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
]