from django.contrib import admin
from myapp.tasks.models import Task, Attachment
from django.contrib.auth.models import Group

# # Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'priority', 'status', 'assigned_to', 'created_by')
    search_fields = ('title', 'description', )
    list_filter = ('priority', 'status', 'assigned_to', 'created_by')
    ordering = ('priority',)
    list_per_page = 3
    fieldsets = (
        ('Task Details', {
            'fields': ('title', 'description', 'due_date', 'priority', 'status', 'assigned_to', 'created_by')
        }),
    )

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'file', 'created_by',)
    search_fields = ('task',)
    list_filter = ('task',)
    # ordering = ('created_at',)
    list_per_page = 3
    fieldsets = (
        ('Attachment Details', {
            'fields': ('task', 'file','created_by')
        }),
    )
    
    
admin.site.register(Task, TaskAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.unregister(Group)

