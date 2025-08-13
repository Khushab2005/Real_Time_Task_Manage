from django.db import models
from myapp.accounts.models import User
from myapp.notifications.constants import NotificationType

# Create your models here.

# ----------------
# Notification Model 
# --------------

class Notification(models.Model):
    receiver = models.ForeignKey(User ,on_delete=models.CASCADE,related_name='notification_receiver')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notification_sender')
    notification_type = models.CharField(max_length=255,choices=NotificationType.choices,default=NotificationType.OTHER)
    message = models.TextField(null=False,blank=False)
    is_read = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.notification_type} - {self.message}"