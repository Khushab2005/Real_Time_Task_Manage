from django.db import models
from  myapp.accounts.models import User
from  myapp.chats.constants import Roomchoice
# Create your models here.

class ChatRoom(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_type = models.CharField(max_length=10, choices=Roomchoice.choices)
    participants = models.ManyToManyField(User, related_name="chatrooms")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_chatrooms")
    
    
    def __str__(self):
        return self.room_name 



        
class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sent_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"

