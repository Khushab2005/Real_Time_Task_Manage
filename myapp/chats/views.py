from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.chats.models import ChatRoom, Message
from rest_framework.permissions import IsAuthenticated
from myapp.accounts.models import User
from myapp.chats.serializers import ChatRoomSerializer , MessageSerializer
from rest_framework import status
from django.views import View
# Create your views here.
class ChatRoomListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        rooms = ChatRoom.objects.filter(participants=user)
        serializer = ChatRoomSerializer(rooms, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChatRoomSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            chatroom = serializer.save()
            return Response(ChatRoomSerializer(chatroom, context={"request": request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in room.participants.all():
            return Response({"error": "You are not a participant of this room"}, status=status.HTTP_403_FORBIDDEN)

        messages = Message.objects.filter(room=room).order_by("timestamp")
        serializer = MessageSerializer(messages, many=True)

        # Exclude current user and return participant names
        participants = room.participants.exclude(id=request.user.id).values_list("name", flat=True)

        return Response({
            "room_name": room.room_name,
            "participants": list(participants),  # convert queryset to list
            "messages": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in room.participants.all():
            return Response({"error": "You are not a participant of this room"}, status=status.HTTP_403_FORBIDDEN)

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, room=room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class chatsroom(View):
    def get(self, request):
        return render(request, 'chatsroom.html')

class chatmessages(View):
    def get(self, request, room_id): 
        return render(request, 'chatmessages.html',{'room_id': room_id})


class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = User.objects.all()
        context = [{"id": user.id, "name": user.name} for user in data]
        return Response(context, status=status.HTTP_200_OK)
    
    
# chats rooom detail view
class chatroomdelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, room_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in room.participants.all():
            return Response({"error": "You are not a participant of this room"}, status=status.HTTP_403_FORBIDDEN)
        
        if room.created_by != request.user:
            return Response({"error": "Only the creator can delete this room"}, status=status.HTTP_403_FORBIDDEN)
        
        room.delete()
        return Response({"msg": "Room deleted successfully."},status=status.HTTP_204_NO_CONTENT)
    
    
    


# chatroom update view 
class chatmessageupdate(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, chat_id):
        try:
            room = Message.objects.get(id=chat_id)
        except Message.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MessageSerializer(room, data=request.data, context={"request": request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
# chatroom delete view
class chatmessagedelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, chat_id):
        try:
            room = Message.objects.get(id=chat_id)
        except Message.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

        if room.sender != request.user:
            return Response({"error": "Only the sender can delete this message"}, status=status.HTTP_403_FORBIDDEN)
        
        room.delete()
        return Response({"msg": "Message deleted successfully."},status=status.HTTP_204_NO_CONTENT)


