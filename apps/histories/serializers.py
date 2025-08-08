from rest_framework import serializers
from .models import HistorySet, History

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'content', 'history_set', 'created_at']
        extra_kwargs = {
            'history_set': {'required': False}
        }

class HistorySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorySet
        fields = ['id', 'title', 'created_at', 'updated_at']