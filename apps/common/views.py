# apps/common/views.py
from rest_framework import viewsets, mixins
from apps.common.responses import ok, created, no_content


class BaseModelViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        query_set = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(query_set, many=True)
        return ok(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return ok(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return created(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return ok(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return no_content()


class BaseListCreateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    def list(self, request, *args, **kwargs):
        query_set = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(query_set, many=True)
        return ok(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return created(serializer.data)