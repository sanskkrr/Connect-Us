import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


@sync_to_async
def save_message(sender, receiver, message):
    from django.contrib.auth.models import User
    from .models import Message

    sender_user = User.objects.get(username=sender)
    receiver_user = User.objects.get(username=receiver)

    Message.objects.create(
        sender=sender_user,
        receiver=receiver_user,
        content=message
    )
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()



  
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        

        sender = self.scope["user"].username   # ✅ define sender
        receiver = self.username             

        print("📩 MESSAGE RECEIVED:", message)
        await save_message(sender, receiver, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.scope["user"].username,
            }
        )

    async def chat_message(self, event):
        print("📤 SENDING TO FRONTEND:", event)

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))
