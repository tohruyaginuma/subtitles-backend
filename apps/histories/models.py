from django.db import models
from django.conf import settings
import uuid

class HistorySet(models.Model):
    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["updated_at"]),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class History(models.Model):
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["history_set", "-created_at"]),
        ]
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    history_set = models.ForeignKey('HistorySet', on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.content[:40] + "…") if len(self.content) > 40 else self.content