from django.contrib import admin
from myapp.notifications.models import Notification
# Register your models here.

#------------------
#Notification Admin customization
#------------------


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id','notification_type','message','receiver','sender','is_read','create_at','update_at')
    search_fields = ('notification_type',)
    list_filter = ('is_read',)
    ordering = ('id',)
    list_per_page = 3
    fieldsets = (
        ('User Information', {
            'fields': ('message','notification_type','receiver', 'sender')
        }),
        ('Permissions', {
            'fields': ('is_read',)
        })
    )


admin.site.register(Notification, NotificationAdmin)


