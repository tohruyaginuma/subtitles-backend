from django.contrib import admin
from .models import Transcribe, TranscribeSet   

# Register your models here.
admin.site.register(Transcribe)
admin.site.register(TranscribeSet)