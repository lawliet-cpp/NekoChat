from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
import redis
from asgiref.sync import sync_to_async
from .models import Room,Message

redis = redis.Redis()

class NekoChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_{}".format(self.room_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
       
    async def disconnect(self, code):
        return await super().disconnect(code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message,
                "username":username
            }
        )

    async def chat_message(self,event):
        content = event["message"]
        username = event["username"]
        await self.save_message(content,username,self.room_name)
        
        await self.send(text_data=json.dumps({
            "message":content,
            "username":username,
        }))

    @sync_to_async
    def save_message(self,content,username,room_name):
        room = Room.objects.get(name=room_name)
        Message.objects.create(content=content,username=username,room=room)

    