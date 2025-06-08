from django.contrib import admin
from .models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_participants', 'created', 'updated']
    filter_horizontal = ['participants']

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'thread', 'text_preview', 'created', 'is_read']
    list_filter = ['is_read', 'created']
    search_fields = ['text', 'sender__username']

    def text_preview(self, obj):
        return obj.text[:40] + ("..." if len(obj.text) > 40 else "")
    text_preview.short_description = 'Text'
