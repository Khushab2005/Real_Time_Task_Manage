from django.contrib import admin
from myapp.chats.models import Message,ChatRoom

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id','name' , 'get_participants')
    def get_participants(self, obj):
        return ", ".join([user.email for user in obj.participants.all()])
    
    get_participants.short_description = "Participants"
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','room', 'sender', 'content', 'timestamp')
    

admin.site.register(Message,MessageAdmin)
admin.site.register(ChatRoom,ChatRoomAdmin)