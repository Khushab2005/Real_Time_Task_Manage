from rest_framework import serializers
from myapp.notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
#------------------
#Notification Serializers 
#------------------
class NotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [ 
            'id',
            'receiver',         
            'sender',         
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
    
    def create(self, validated_data):
        request_user = self.context['request'].user
        validated_data['sender'] = request_user  

        notification = Notification.objects.create(**validated_data)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{notification.receiver.id}",
            {
                "type": "send_notification",
                "content": {
                    "id": notification.id,
                    "message": notification.message,
                    "notification_type": notification.notification_type,
                    "is_read": notification.is_read,
                },
            }
        )

        return notification

