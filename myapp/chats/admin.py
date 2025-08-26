from django.contrib import admin
from myapp.chats.models import Message,ChatRoom

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id','room_name' , 'room_type','get_participants' ,'created_by')
    def get_participants(self, obj):
        return ", ".join([user.name for user in obj.participants.all()])
    
    get_participants.short_description = "Participants"
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','room', 'sender', 'content', 'timestamp')
    

admin.site.register(Message,MessageAdmin)
admin.site.register(ChatRoom,ChatRoomAdmin)