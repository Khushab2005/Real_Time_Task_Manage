from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from myapp.notifications.serializers import NotificationSerializers
from myapp.notifications.models import Notification
from myapp.accounts.constants import Rolechoice
from rest_framework.response import Response
from myapp.accounts.models import User  
from myapp.tasks.models import Task
from myapp.tasks.constants import StatusChoice
from django.db  import models
# Create your views here.


#------------------
#Notification List View
#------------------
class NotificationListView(ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        request_user = self.request.user
        if request_user.role == Rolechoice.ADMIN:
            return Notification.objects.all() 
        return Notification.objects.filter(receiver= self.request.user)
    
    
 

#------------------
#Notification Read View
#------------------
class NotificationReadView(UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.receiver != request.user:
            return Response({"details":"You Are Not Receiver this Message"})
        if notification.is_read is True:
            return Response({"details":"This Message Already Read ."})
        notification.is_read = True
        notification.save()
        serializers = self.get_serializer(notification)
        return Response(serializers.data)

#------------------
#Analytics & Reports 
#------------------
class AnalyticsView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
          # Only Admins and Managers allowed
        if request.user.role not in [Rolechoice.ADMIN, Rolechoice.MANAGER]:
            return Response({"error": "Not authorized"})

        employee_id = kwargs.get("pk")

        # Check if the user exists and is an employee
        try:
            employee = User.objects.get(id=employee_id, role=Rolechoice.EMPLOYEE)
        except User.DoesNotExist:
            return Response({"error": "Invalid employee ID"} )

        # Manager should not be able to see Admin/Manager reports
        if request.user.role == Rolechoice.MANAGER and employee.role != Rolechoice.EMPLOYEE:
            return Response({"error": "Managers can only view employee reports"})

        # Get tasks of the employee
        tasks = Task.objects.filter(assigned_to=employee)

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status=StatusChoice.COMPLETED).count()
        pending_tasks = tasks.filter(status=StatusChoice.PENDING).count()
        in_progress_tasks = tasks.filter(status=StatusChoice.IN_PROGRESS).count()

        completed_on_time = tasks.filter(
            status=StatusChoice.COMPLETED,
            updated_at__lte=models.F("due_date")
        ).count()


        completed_late = tasks.filter(
            status=StatusChoice.COMPLETED,
            updated_at__gt=models.F("due_date")
        ).count()

        return Response({
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_on_time": completed_on_time,
            "completed_late": completed_late,
        })