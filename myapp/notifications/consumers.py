from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print(f"User {self.user} connected")
        if self.user.is_authenticated:
            print(f"User {self.user} authenticated")
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            print(f"User {self.user} joined group {self.group_name}")
        else:
            # Reject the connection if user is not authenticated
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        """
        Receives event from channel layer and sends it to WebSocket
        """
        await self.send(text_data=json.dumps(event["content"]))
