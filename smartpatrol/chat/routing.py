# We need to create a routing configuration for the chat app that has a route to the consumer. Create a new file chat/routing.py.
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # We call the as_asgi() classmethod in order to get an ASGI application that will instantiate an instance of our consumer for each user-connection.
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
