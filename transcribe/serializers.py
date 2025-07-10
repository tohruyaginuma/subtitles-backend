from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Transcribe, TranscribeSet
from rest_framework.response import Response

class TranscribeSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscribeSet
        fields = '__all__'
    
    def list(self, request):
        transcribe_set = TranscribeSet.objects.filter(user_id=request.user.id)
        serializer = TranscribeSetSerializer(transcribe_set, many=True)
        return Response(serializer.data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance