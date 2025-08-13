from rest_framework import serializers
from myapp.notifications.models import Notification

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
        data = Notification.objects.create(**validated_data)
        return data    