# when Channels accepts a WebSocket connection, it consults the root routing configuration to lookup a consumer, and then calls various functions on the consumer to handle events from the connection.
# consumer that accepts WebSocket connections on the path /ws/chat/ROOM_NAME/ that takes any message it receives on the WebSocket and echos it back to the same WebSocket.
import json
from channels.generic.websocket import WebsocketConsumer

# this file as 3 methods
class ChatConsumer(WebsocketConsumer):
    # this first metod only initiates a connection
    def connect(self):
        self.accept()

    # on disconnect do nothing(pass)
    def disconnect(self, close_code):
        pass


    def receive(self, text_data):
        # grab the textdata and convert into json
        text_data_json = json.loads(text_data)
        # since json is a dictionary access the key and assign it to the message
        message = text_data_json['message']

        # now we send the message inside a json dump
        self.send(text_data=json.dumps({
            'message': message
        }))
