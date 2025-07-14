from django.db import models
import uuid
from accounts.models import User
# Create your models here.
class Transcribe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sentence = models.TextField()
    transcribe_set_id = models.ForeignKey('TranscribeSet', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sentence

class TranscribeSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title