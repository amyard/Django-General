from django.contrib import admin
from .models import Task



class TaskAdmin(admin.ModelAdmin):
    list_display = ['title','project', 'user', 'timestamp', 'priority', 'status']
    list_filter = ['timestamp', 'priority', 'status']
    list_editable = ['timestamp','priority', 'status']
    date_hierarchy = 'timestamp'

    def user(self, obj):
        return obj.project.user

admin.site.register(Task, TaskAdmin)