from rest_framework import serializers
from myapp.tasks.models import Task, Attachment
from myapp.accounts.constants import Rolechoice
from myapp.accounts.models import User
from myapp.notifications.models import Notification
from myapp.notifications.constants import NotificationType





        
        
# Create your models here.

# ----------------
# Task Model of serialization
# ----------------
class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    created_by = serializers.CharField(source='created_by.name', read_only=True)

    class Meta: 
        model = Task 
        fields = [ 'id' ,'title','file_of_task' ,'description', 'due_date', 'priority', 'status', 'assigned_to','created_by']
        read_only_fields = ['created_by', 'created_at']
        
    def validate(self, attrs ):
        request_user = self.context['request'].user
        assigned_to = attrs.get('assigned_to')
        title = attrs.get('title')
        
        if Task.objects.filter(title = title).exists():
            raise serializers.ValidationError("Title already exists.")
            
        
        # Employee cannot assign or create tasks
        if request_user.role == Rolechoice.EMPLOYEE:
            raise serializers.ValidationError("Employees cannot assign or create tasks.")

        # Manager assigning a task
        if request_user.role == Rolechoice.MANAGER:
            if assigned_to and assigned_to.role != Rolechoice.EMPLOYEE:
                raise serializers.ValidationError("Managers can only assign tasks to employees.")
            

        return attrs
    
    
    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user
        task = Task.objects.create(**validated_data)

        # Create notification for assigned user
        if task.assigned_to:
            Notification.objects.create(
                receiver=task.assigned_to,
                sender=request_user,
                notification_type=NotificationType.TASKS_ASSIGN,
                message=task.title
            )
        return task
    
    
    
    def update(self, instance, validated_data):
        request_user = self.context['request'].user

        # Creator can update everything
        if instance.created_by == request_user:
            return super().update(instance, validated_data)
        
        # Admin can update everything
        elif request_user.role == Rolechoice.ADMIN:
            return super().update(instance, validated_data)

        # Assigned user can only update status
        elif instance.assigned_to == request_user:
            allowed_fields = ['status']
            if not all(field in allowed_fields for field in validated_data.keys()):
                raise serializers.ValidationError("You can only update the status of this task.")
            return super().update(instance, validated_data)

        # Nobody else can update
        else:
            raise serializers.ValidationError("You are not allowed to update this task.")



# ----------------
# Attachment Model of serialization
# ----------------
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'attach_file', 'task', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def validate(self, data):
        request_user = self.context['request'].user

        if self.instance is None:  # only on create
            task = data.get('task')
            if not task:
                raise serializers.ValidationError("Task is required.")
            if Attachment.objects.filter(task=task).exists():
                raise serializers.ValidationError("Attachment for this task already exists.")
            if request_user.role == Rolechoice.ADMIN:
                raise serializers.ValidationError("Admins are not allowed to upload attachments.")
            if task.assigned_to != request_user:
                raise serializers.ValidationError("You can only upload attachments to tasks assigned to you.")

        return data

    
    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user
        return Attachment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.attach_file = validated_data.get('attach_file', instance.attach_file)
        instance.save()
        return instance
    