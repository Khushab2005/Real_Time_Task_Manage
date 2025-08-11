from django.db import models
from myapp.accounts.models import User
<<<<<<< Updated upstream
from myapp.tasks.constants import PriorityChoice , StatusChoice
import os
# Create your models here.


# ----------------
# Function to define upload path for task files
# ----------------
def task_file_upload_path_title(instance, filename):
    name = instance.title.replace(" ", "_")
    ext = filename.split('.')[-1]
    new_filename = f"{name}.{ext}"
    return os.path.join("Task_files", name, new_filename)    


# ----------------
# Task Model 
# ----------------
class Task(models.Model):
    title = models.CharField(max_length=255,unique=True)
    file_of_task = models.FileField(upload_to=task_file_upload_path_title, blank=True, null=True)
=======
from myapp.tasks.constants import PriorityChoice, StatusChoice
import os
# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=255)
>>>>>>> Stashed changes
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
<<<<<<< Updated upstream
    priority = models.CharField(max_length=15, choices=PriorityChoice, default=PriorityChoice.LOW)
    status = models.CharField(max_length=15, choices=StatusChoice, default=StatusChoice.PENDING)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE  )
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE )

    def __str__(self):
        return self.title
    
# ----------------
# Upload Path Function for attach_file  
# ----------------

def task_file_upload_path_name(instance, filename):
    name = instance.created_by.name.replace(" ", "_")
    ext = filename.split('.')[-1]
    new_filename = f"{name}.{ext}"
    return os.path.join("Task_Attachment", name, new_filename)    

# ----------------
# Attachment Model 
# ----------------
class Attachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    attach_file = models.FileField(upload_to=task_file_upload_path_name, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='attachments_received', on_delete=models.CASCADE)


=======
    priority = models.CharField(max_length=15,choices=PriorityChoice,default=PriorityChoice.LOW)
    status = models.CharField(max_length=15, choices=StatusChoice, default=StatusChoice.PENDING)
    assigned_by = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE,null=True)
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.title
    
    

def upload_path(instance, filename):
    taskower = instance.task_owner.name.replace(" ", "_")
    uploadby = instance.uploaded_by.name.replace(" ", "_")
    ext = filename.split('.')[-1]
    new_filename = f"{uploadby}.{ext}" 
    return os.path.join("Task_Attachement", taskower, new_filename)



class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=upload_path , blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_attachments',null=True)
    task_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_task_attachments', null=True)

    def __str__(self):
        return f"Title :- {self.task.title} - Upload by :- {self.uploaded_by}"
    
  
    
>>>>>>> Stashed changes
