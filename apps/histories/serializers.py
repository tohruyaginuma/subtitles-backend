from rest_framework import serializers
from .models import HistorySet, History

class HistorySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorySet
        fields = ['id', 'title', 'created_at', 'updated_at']
        read_only_fields = ["id", "created_at", "updated_at"]

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'content', 'history_set', 'created_at']
        read_only_fields = ["id", "history_set", "created_at"]