from django.contrib import admin

# Register your models here.
from myapp.models import *

admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(TaskActivityLog)
admin.site.register(Notification)
admin.site.register(FileAttachment)

