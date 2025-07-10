from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import TranscribeSet
from .serializers import TranscribeSetSerializer


class TranscribeSetViewSet(viewsets.ModelViewSet):
    queryset = TranscribeSet.objects.all()
    serializer_class = TranscribeSetSerializer
    permission_classes = [permissions.IsAuthenticated]