from django.contrib import admin
from myapp.accounts.models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'role','is_staff', 'is_active')
    search_fields = ('name', 'email')
    list_filter = ('role','is_staff', 'is_active')
    ordering = ('role',)
    list_per_page = 3
    fieldsets = (
        ('User Information', {
            'fields': ('name','profile', 'email', 'role')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active')
        })
    )
    
admin.site.site_header = "Real Time Task Management System"
admin.site.site_title = "Real Time Task Management"
admin.site.index_title = "Welcome to Real Time Task Management System"




admin.site.register(User, UserAdmin)
