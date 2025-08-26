from django.urls import path
from myapp.chats.views import ChatRoomListView , ChatMessageView,AllUsersView,chatsroom,chatmessages

urlpatterns = [
    path('',chatsroom.as_view(), name='chatsroom'),
    path('chatroomlist/', ChatRoomListView.as_view(), name='chatroomlist'),
    path('chatmessagespage/<int:room_id>/',chatmessages.as_view(), name='chatmessagespage'),
    path('chatmessage/<int:room_id>/', ChatMessageView.as_view(), name='chatmessage'),
    path('alldata/', AllUsersView.as_view(), name='AllUsersView'),
]
