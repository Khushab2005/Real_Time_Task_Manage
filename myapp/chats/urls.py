from django.urls import path
from myapp.chats.views import ChatRoomListView , ChatMessageView,chatsroom

urlpatterns = [
    path('',chatsroom, name='chatsroom'),
    path('chatroomlist/', ChatRoomListView.as_view(), name='chatroomlist'),
    path('chatmessage/<int:room_id>/', ChatMessageView.as_view(), name='chatmessage'),
]
