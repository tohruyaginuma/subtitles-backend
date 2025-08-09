from rest_framework import viewsets, mixins
from .models import HistorySet, History
from .serializers import HistorySetSerializer, HistorySerializer
from apps.common.responses import ok, no_content, created
from apps.common.views import BaseModelViewSet, BaseListCreateViewSet

class HistorySetViewSet(BaseModelViewSet):
    serializer_class = HistorySetSerializer

    def get_queryset(self):
        return HistorySet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HistoryViewSet(BaseListCreateViewSet):
    serializer_class = HistorySerializer

    def get_queryset(self):
        hs_id = self.kwargs["history_set_id"]
        return History.objects.filter(history_set_id=hs_id)

    def perform_create(self, serializer):
        hs_id = self.kwargs["history_set_id"]
        serializer.save(history_set_id=hs_id)