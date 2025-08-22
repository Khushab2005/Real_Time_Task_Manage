from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.chats.models import ChatRoom, Message
from rest_framework.permissions import IsAuthenticated
from myapp.accounts.models import User
from myapp.chats.serializers import ChatRoomSerializer , MessageSerializer
from rest_framework import status
# Create your views here.

class ChatRoomListView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        rooms = ChatRoom.objects.filter(participants=user)
        serializer = ChatRoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializers = ChatRoomSerializer(data=request.data, context={'request': request})
        if serializers.is_valid():
            chatroom = serializers.save()
            return Response(ChatRoomSerializer(chatroom).data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request , room_id):
        message = Message.objects.filter(room_id=room_id).order_by('timestamp')
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def chatsroom(request):
    data = User.objects.all()
    return render(request, 'chatsroom.html', {'data': data})