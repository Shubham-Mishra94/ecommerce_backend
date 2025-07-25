import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_authenticated:
           self.user_id = self.scope['url_route']['kwargs']['user_id']
           self.group_name = f'user_{self.user_id}_orders'

           await self.channel_layer.group_add(self.group_name, self.channel_name)
           await self.accept()
        else:
            await self.close()


    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
           await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def order_status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'order_status_update',
            'order_id': event['order_id'],
            'new_status': event['new_status']
        }))



