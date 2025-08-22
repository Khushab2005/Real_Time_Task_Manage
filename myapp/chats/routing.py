from django.urls import re_path
from myapp.chats.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chats/(?P<room_id>\w+)/$", ChatConsumer.as_asgi()),
]
