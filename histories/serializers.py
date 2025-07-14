from rest_framework import serializers
from histories.models import HistorySet

class HistorySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorySet
        fields = ['id', 'title', 'created_at']