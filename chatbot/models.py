from django.db import models
from django.contrib.auth.models import User

class ChatBot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_input = models.TextField()
    gemini_output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} asked at {self.created_at}"
