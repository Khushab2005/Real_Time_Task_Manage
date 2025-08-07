from django.contrib import admin
from myapp.tasks.models import Task, Attachment
from django.contrib.auth.models import Group

# # Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_of_task','description', 'due_date', 'priority', 'status', 'assigned_to', 'created_by')
    search_fields = ('title', 'description', )
    list_filter = ('priority', 'status', 'assigned_to', 'created_by')
    ordering = ('priority',)
    list_per_page = 3
    fieldsets = (
        ('Task Details', {
            'fields': ('title','file_of_task', 'description', 'due_date', 'priority', 'status', 'assigned_to', 'created_by')
        }),
    )

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'attach_file', 'created_by','created_at')
    search_fields = ('task',)
    list_filter = ('task',)
    # ordering = ('created_at',)
    list_per_page = 3
    fieldsets = (
        ('Attachment Details', {
            'fields': ('task', 'attach_file','created_by')
        }),
    )
    
    
admin.site.register(Task, TaskAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.unregister(Group)

