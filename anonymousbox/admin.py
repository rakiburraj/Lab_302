from django.contrib import admin
from .models import AnonymousMessage

@admin.register(AnonymousMessage)
class AnonymousMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'short_message', 'is_replied', 'created_at')
    list_filter = ('is_replied', 'created_at')
    search_fields = ('name', 'email', 'message')

    def short_message(self, obj):
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")
    short_message.short_description = 'Message'
