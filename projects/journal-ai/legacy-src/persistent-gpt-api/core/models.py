from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid



# Custom User Model
class CustomUser(AbstractUser):
    # Additional fields as needed
    profile_pic = models.URLField(blank=True, null=True)
    oauth_provider = models.CharField(max_length=50, blank=True, null=True)
    unique_identifier = models.CharField(max_length=150, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.unique_identifier:
            self.unique_identifier = str(uuid.uuid4())  
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.username}"




# Chat Session Model
class ChatSession(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='active')  # 'active', 'inactive'
    session_data = models.JSONField() 

    # EXAMPLE session_data
    # {
    # "messages": [
    #     {"text": "User's message", "timestamp": "2024-01-13T12:00:00"},
    #     {"text": "GPT's response", "timestamp": "2024-01-13T12:00:10"},
    #     ...
    #   ]
    # }

    def __str__(self):
        return f"Session {self.session_id} - User {self.user.username}"





# Chat Message Model
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message at {self.timestamp} in Session {self.session.session_id}"
