from rest_framework import serializers
from myapp.notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

#------------------
#Notification Serializers 
#------------------
class NotificationSerializers(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    class Meta:
        model = Notification
        fields = [ 
            'id',
            'receiver',         
            'sender',   
            'sender_name',      
            'notification_type',         
            'message',      
            'is_read',   
            'create_at',      
            'update_at',              
        ]
        read_only_fields  = ['id','create_at','sender']
        
    def validate(self, attrs):
        sender = self.context['request'].user
        receiver = attrs.get('receiver')
        if sender == receiver:
            raise serializers.ValidationError("Sender and Receiver cannot be the same user.")
        return attrs
    

