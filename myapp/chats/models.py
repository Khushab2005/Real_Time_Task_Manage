from django.db import models
from  myapp.accounts.models import User
# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=255,unique=True)
    participants = models.ManyToManyField(User,related_name="chat_rooms")
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.name}: {self.content[:30]}"

