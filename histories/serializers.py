from rest_framework import serializers
from histories.models import TranscribeSet

class TranscribeSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscribeSet
        fields = ['id', 'title', 'created_at']