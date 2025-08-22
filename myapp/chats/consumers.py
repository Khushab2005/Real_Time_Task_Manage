import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from myapp.chats.models import ChatRoom , Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]   # get from URL
        self.room_group_name = f"chat_{self.room_id}"                 # group name


        # join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = self.scope["user"]
        
        if not await self.is_participant(sender):
            await self.send(text_data=json.dumps({"error": "You are not a participant in this room."}))
            return

        # save to DB
        msg_obj = await self.create_message(sender , self.room_id, message)

        # send to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg_obj["message"],
                "sender": msg_obj["sender"],
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))


    @database_sync_to_async
    def create_message(self, sender, room, message):
        msg = Message.objects.create(
            sender=sender,
            room_id=room,
            content=message
        )
        return {
            "message": msg.content,
            "sender": msg.sender.email
        }


        
    @database_sync_to_async
    def is_participant(self, user):
        try:
            room = ChatRoom.objects.get(id=self.room_id)
            return room.participants.filter(id=user.id).exists()
        except ChatRoom.DoesNotExist:
            return False
