# when Channels accepts a WebSocket connection, it consults the root routing configuration to lookup a consumer, and then calls various functions on the consumer to handle events from the connection.
# consumer that accepts WebSocket connections on the path /ws/chat/ROOM_NAME/ that takes any message it receives on the WebSocket and echos it back to the same WebSocket.
import json
# this enables the message to be seen on both sides of the room (in coordination with redis runing on docker)
# docker is a container that we can run several applications at the same time(more like virtualization)
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

from channels.generic.websocket import AsyncWebsocketConsumer


# this file as 3 methods
class ChatConsumer(AsyncWebsocketConsumer):
    # this first metod only initiates a connection
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

         # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


 # Receive message from WebSocket
    async def receive(self, text_data):
        # grab the textdata and convert into json
        text_data_json = json.loads(text_data)
        # since json is a dictionary access the key and assign it to the message
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


     # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
