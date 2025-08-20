from rest_framework import viewsets, mixins
from .models import HistorySet, History
from .serializers import HistorySetSerializer, HistorySerializer
from apps.common.responses import ok, no_content, created
from apps.common.pagination import CustomLimitOffsetPagination

class HistorySetViewSet(viewsets.ModelViewSet):
    serializer_class = HistorySetSerializer
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        return HistorySet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        query_set = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(query_set)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(query_set, many=True)
        return ok(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return ok(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return created({"id": serializer.data["id"]})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ok({"id": serializer.data["id"], "title": serializer.data["title"]})

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return no_content()

class HistoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = HistorySerializer
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        hs_id = self.kwargs["history_set_id"]
        return History.objects.filter(history_set_id=hs_id)

    def perform_create(self, serializer):
        hs_id = self.kwargs["history_set_id"]
        serializer.save(history_set_id=hs_id)

    def list(self, request, *args, **kwargs):
        query_set = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(query_set)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(query_set, many=True)
        return ok({"data": serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return created()