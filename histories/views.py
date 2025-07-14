from rest_framework import viewsets, permissions, mixins, status
from django.shortcuts import get_object_or_404
from histories.models import HistorySet
from histories.serializers import HistorySetSerializer
from rest_framework.response import Response

class HistorySetViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = HistorySetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HistorySet.objects.filter(user_id=self.request.user.id)

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().order_by('-created_at')
            serializer = self.get_serializer(queryset, many=True)
            return Response({"data": serializer.data, "error": None}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data": None, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)