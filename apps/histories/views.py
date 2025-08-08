from rest_framework import viewsets, permissions, mixins
from .models import HistorySet, History
from .serializers import HistorySetSerializer, HistorySerializer

class HistoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        history_set_id = self.kwargs["history_set_id"]
        return History.objects.filter(history_set=history_set_id)
    
    def perform_create(self, serializer):
        history_set_id = self.kwargs["history_set_id"]
        serializer.save(history_set=HistorySet.objects.get(id=history_set_id))

class HistorySetViewSet(viewsets.ModelViewSet):
    serializer_class = HistorySetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HistorySet.objects.filter(user=self.request.user.id)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
