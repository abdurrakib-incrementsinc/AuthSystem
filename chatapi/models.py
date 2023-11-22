from django.db import models
from authsystem.models import BaseModel
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid
# Create your models here.


class Conversation(BaseModel):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_one')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_two')
    is_active = models.BooleanField(default=True)
    name = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return f"{self.user_one}-{self.user_two}"


class Message(BaseModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conv_msg')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('created_at',)

