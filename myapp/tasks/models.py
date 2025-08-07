from django.db import models
from myapp.accounts.models import User
from myapp.tasks.constants import PriorityChoice , StatusChoice
import os
# Create your models here.

# Task Model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.CharField(max_length=15, choices=PriorityChoice, default=PriorityChoice.LOW)
    status = models.CharField(max_length=15, choices=StatusChoice, default=StatusChoice.PENDING)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE  )
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE )

    def __str__(self):
        return self.title

# Upload Path Function for FileField  
def upload_path(instance, filename):
    name1 = instance.created_by.name.replace(" ", "_")
    ext = filename.split('.')[-1]
    new_filename = f"{name1}.{ext}"
    return os.path.join("Task_Attachment", name1, new_filename)    


# Attachment Model
class Attachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='attachments_received', on_delete=models.CASCADE)


