from django.contrib import admin
from .models import Conversation, Message
# Register your models here.


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1  # Number of empty message forms to display


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user_one', 'user_two', 'is_active', 'name')
    inlines = [MessageInline]


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message)
