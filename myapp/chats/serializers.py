from rest_framework import serializers
from myapp.chats.models import ChatRoom, Message
from myapp.accounts.models import User

class ChatRoomSerializer(serializers.ModelSerializer):
    receiver_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    participants = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ["id", "name", "receiver_id", "participants"]

    def create(self, validated_data):
        receiver_ids = validated_data.pop("receiver_id", [])
        request_user = self.context["request"].user

        chatroom = ChatRoom.objects.create(**validated_data)

      
        users = User.objects.filter(id__in=receiver_ids)
        chatroom.participants.set(list(users) + [request_user])

        return chatroom

    def get_participants(self, obj):
        return [u.email for u in obj.participants.all()] 

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.email')
    class Meta:
        model = Message
        fields = ['id', 'sender', 'room','content', 'timestamp']