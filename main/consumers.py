from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
import redis
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
        message = "{}_{}".format(content,username)
        redis.sadd(self.room_name,message)
        
        
        await self.send(text_data=json.dumps({
            "message":content,
            "username":username,
        }))