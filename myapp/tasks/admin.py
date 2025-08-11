from django.contrib import admin
<<<<<<< Updated upstream
from myapp.tasks.models import Task, Attachment
from django.contrib.auth.models import Group

# # Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'file_of_task','description', 'due_date', 'priority', 'status', 'assigned_to', 'created_by')
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
    list_display = ('id','task', 'attach_file', 'created_by','created_at')
    search_fields = ('task',)
    list_filter = ('task',)
    # ordering = ('created_at',)
    list_per_page = 3
    fieldsets = (
        ('Attachment Details', {
            'fields': ('task', 'attach_file','created_by')
        }),
    )
    
    
=======
from myapp.tasks.models import Task,Attachment
from django.contrib.auth.models import Group
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'priority','status','assigned_by','assigned_to')
    search_fields = ('title', 'description')
    list_filter = ('priority','status','assigned_by','assigned_to')
    ordering = ('priority',)
    list_per_page = 3
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'due_date', 'priority','status','assigned_by','assigned_to')
        }),
    )
    
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'file' , 'created_at' , 'uploaded_by', 'task_owner')
    search_fields = ('task', 'file')
    list_filter = ('task',)
    ordering = ('task',)
    list_per_page = 3
    fieldsets = (
        ('Attachment Information', {
            'fields': ('task', 'file')
        }),
        ('User Information', {
            'fields': ('uploaded_by', 'task_owner')
        }),
       
    )
    


>>>>>>> Stashed changes
admin.site.register(Task, TaskAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.unregister(Group)

