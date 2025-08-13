from django.shortcuts import render
from rest_framework.generics import CreateAPIView,UpdateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from myapp.notifications.serializers import NotificationSerializers
from myapp.notifications.models import Notification
from myapp.accounts.constants import Rolechoice
from rest_framework.response import Response
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
#Notification Create View
#------------------   
class NotificationCreateView(CreateAPIView):
    serializer_class = NotificationSerializers
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(sender = self.request.user)
        

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

         
        