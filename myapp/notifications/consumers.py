from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from myapp.notifications.models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        receiver_id = data["receiver_id"]
        message = data["message"]
        notification_type = data["notification_type"]

        # Prevent sending notification to self
        if receiver_id == self.user.id:
            await self.send(text_data=json.dumps({"error": "You cannot send a notification to yourself."}))
            return

        # Create notification in DB
        notification = await self.create_notification(receiver_id, message, notification_type)

        # Send to receiver group
        await self.send_to_group(notification)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["content"]))

    @database_sync_to_async
    def create_notification(self, receiver_id, message, notification_type):
        return Notification.objects.create(
            sender=self.user,
            receiver_id=receiver_id,
            message=message,
            notification_type=notification_type
        )

    @database_sync_to_async
    def get_receiver_id(self, notification):
        return notification.receiver.id

    async def send_to_group(self, notification):
        receiver_id = await self.get_receiver_id(notification)
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            f"user_{receiver_id}",
            {
                "type": "send_notification",
                "content": {
                    "id": notification.id,
                    "message": notification.message,
                    "notification_type": notification.notification_type,
                    "is_read": notification.is_read,
                }
            }
        )
