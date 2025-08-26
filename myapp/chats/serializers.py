from rest_framework import serializers
from myapp.chats.models import ChatRoom, Message
from myapp.accounts.models import User

class ChatRoomSerializer(serializers.ModelSerializer):
    receiver_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    participants = serializers.SerializerMethodField()
    created_by = serializers.CharField(source='created_by.name', read_only=True)

    class Meta:
        model = ChatRoom
        fields = ["id", "room_name", "receiver_id", "participants","room_type","created_by"]
        extra_kwargs = {
            "room_name": {"required": False,"allow_blank": True},  
            "room_type": {"required": False, "read_only": True},
        }

    def create(self, validated_data):
        receiver_ids = validated_data.pop("receiver_id", [])
        request_user = self.context["request"].user

        users = list(User.objects.filter(id__in=receiver_ids))
        all_users = users + [request_user]
        
        if request_user.id in receiver_ids:
            raise serializers.ValidationError({"receiver_id": "You cannot add yourself as a receiver."})

  
        
        room_type = "single" if len(all_users) == 2 else "group"
        
        room_name = validated_data.get("room_name")
        
        if not room_name:
            if room_type == "single":
                receiver = [u for u in all_users if u != request_user][0]
                room_name = f"{request_user.name}_chats_with_{receiver.name}"
            else:
                if not room_name:
                    raise serializers.ValidationError({"room_name": "Room name is required for group chats."})
                else:
                    room_name = self.initial_data.get("room_name")
        
        if ChatRoom.objects.filter(room_name=room_name).exists():
            raise serializers.ValidationError({"room_name": "Room with this name already exists."})
        
        chatroom = ChatRoom.objects.create(
            room_name=room_name,
            room_type=room_type,
            created_by=request_user
        )
        
        chatroom.participants.set(all_users)

        return chatroom


    def get_participants(self, obj):
        return [u.name for u in obj.participants.all()] 
    
   

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ['id', 'sender', 'room','content', 'timestamp']