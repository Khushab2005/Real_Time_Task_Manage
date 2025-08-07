from rest_framework import serializers
from myapp.tasks.models import Task, Attachment
from myapp.accounts.constants import Rolechoice




        
        
# Create your models here.

# ----------------
# Task Model of serialization
# ----------------



class TaskSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Task 
        fields = [ 'id' ,'title','file_of_task' ,'description', 'due_date', 'priority', 'status', 'assigned_to', 'created_by']
        read_only_fields = ['created_by', 'created_at']
        
    def validate(self, data):
        request_user = self.context['request'].user
        assigned_to = data.get('assigned_to')
        
        if request_user.role == Rolechoice.EMPLOYEE:
            raise serializers.ValidationError("Employees cannot create tasks.")

        if request_user.role == Rolechoice.ADMIN and assigned_to.role == Rolechoice.ADMIN:
            raise serializers.ValidationError("Admin cannot assign tasks to another Admin.")

        if request_user.role == Rolechoice.MANAGER and assigned_to.role != Rolechoice.EMPLOYEE:
            raise serializers.ValidationError("Manager can only assign tasks to Employees.")
        return data
    
    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['created_by']  = request_user
        return Task.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        
        #only creator can update
        if instance.created_by != request_user:
            raise serializers.ValidationError("You are not the creator of this task.")
        
        # Employees can only update status
        if request_user.role == Rolechoice.EMPLOYEE:
            if 'status' in validated_data:
                instance.status = validated_data['status']
                instance.save()
                return instance
            raise serializers.ValidationError("Employees can only update status.")
        
        # Managers can update their own tasks or tasks assigned to their employees
        if request_user.role == Rolechoice.MANAGER:
            if instance.created_by != request_user and instance.assigned_to != request_user:
                raise serializers.ValidationError("Managers can only update their own tasks or tasks assigned to their employees.")
    
        for i in ['title','file_of_task' ,'description', 'due_date', 'priority', 'status', 'assigned_to']:
            if i in validated_data:
                setattr(instance, i , validated_data[i])
                
        instance.save()
        return instance


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
        task = data.get('task')
        
        # Admins are not allowed to upload attachments
        if request_user.role == Rolechoice.ADMIN:
            raise serializers.ValidationError("Admins are not allowed to upload attachments.")

        # Only allow upload if task is assigned to the current user
        if task.assigned_to != request_user:
            raise serializers.ValidationError("You can only upload attachments to tasks assigned to you.")
  
        return data
    
    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['created_by'] = request_user
        return Attachment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.file = validated_data.get('attach_file', instance.file)
        instance.save()
        return instance