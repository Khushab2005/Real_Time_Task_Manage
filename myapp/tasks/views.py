from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView  ,RetrieveUpdateAPIView  ,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from myapp.tasks.models import Task, Attachment
from myapp.tasks.serializers import TaskSerializer, AttachmentSerializer
from myapp.accounts.models import User
from rest_framework import status
from rest_framework.response import Response
from myapp.accounts.constants import Rolechoice
from rest_framework.exceptions import PermissionDenied

# Create your views here.


# ----------------
# Task views
# ----------------
class TaskCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        request_user = self.request.user
        if request_user.role == Rolechoice.ADMIN :
            return Task.objects.all()
        elif request_user.role == Rolechoice.MANAGER:
            return Task.objects.filter(created_by=request_user)
        return Task.objects.none() 
    
    def perform_create(self, serializer):
        serializer.save()

      
# ----------------
# Task Assigned views
# ----------------   
class TaskAssignedView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        request_user = self.request.user
        if request_user.role == Rolechoice.ADMIN :
            return Task.objects.none()
        elif request_user.role == Rolechoice.MANAGER:
            return  Task.objects.filter(assigned_to=request_user)
        elif request_user.role == Rolechoice.EMPLOYEE:
            return Task.objects.filter(assigned_to=request_user)
        return Task.objects.none() 
        
        
          
# ----------------
# Task Modify views
# ----------------
class TaskModifyView(RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        request_user = self.request.user
        
        if request_user.role == Rolechoice.EMPLOYEE:
            # Allow if employee is either the creator OR assigned to the task
            if obj.created_by != request_user and obj.assigned_to != request_user:
                raise PermissionDenied("You do not have permission to view or edit this task.")
        
        return obj

    
    
        
    def perform_update(self, serializer):
        request_user = self.request.user
        instance = self.get_object()

        if request_user.role == Rolechoice.EMPLOYEE:
            # Allow only if they are assigned or the creator
            if instance.created_by != request_user and instance.assigned_to != request_user:
                raise PermissionDenied("You do not have permission to update this task.")

            # Restrict to only status updates
            allowed_fields = ['status']
            for field in serializer.validated_data.keys():
                if field not in allowed_fields:
                    raise PermissionDenied("You can only update the status of the task.")

        serializer.save()

 #
   
   
   
# ----------------
# Task Delete views
# ----------------   
class TaskDeleteView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def delete(self, request , pk):
        try:
            task = Task.objects.get(pk=pk)
            if task.created_by != request.user and request.user.role != Rolechoice.ADMIN:
                return Response({"error": "You do not have permission to delete this task."}, status=status.HTTP_403_FORBIDDEN)
            task.delete()
            return Response({"msg": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT
            )
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)


# ----------------
# Task Attachment views
# ----------------    
class TaskAttachmentView(ListCreateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        request_user = self.request.user
        if request_user.role == Rolechoice.ADMIN :
            return Attachment.objects.none()
        elif request_user.role == Rolechoice.MANAGER:
            return  Attachment.objects.filter(task__assigned_to=request_user)
        elif request_user.role == Rolechoice.EMPLOYEE:
            return Attachment.objects.filter(task__assigned_to=request_user)
        return Attachment.objects.none() 
    

# ----------------
# Task Attachment Modify views
# ----------------
class TaskAttchmentModifyView(RetrieveUpdateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        request_user = self.request.user
        
        if request_user.role == Rolechoice.ADMIN:
            raise PermissionDenied("Admins are not allowed to modify attachments.")
        
        if obj.task.assigned_to != request_user:
            raise PermissionDenied("You can only modify attachments for tasks assigned to you.")
        
        return obj
    
    def perform_update(self, serializer):
        serializer.save()
  
# ----------------
# Task Attachment Delete views
# ----------------
class TaskAttachmentDeleteView(DestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            attachment = Attachment.objects.get(pk=pk)  
            if attachment.task.assigned_to != request.user and request.user.role != Rolechoice.ADMIN:
                return Response({"error": "You do not have permission to delete this attachment."}, status=status.HTTP_403_FORBIDDEN)
            attachment.delete()
            return Response({"msg": "Attachment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Attachment.DoesNotExist:
            return Response({"error": "Attachment not found."}, status=status.HTTP_404_NOT_FOUND)

    
     
