from django.contrib import admin
from .models import Reaction


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'reaction_type', 'emoji_display', 'content_type', 'object_id', 'content_object_display', 'created_at')
    list_filter = ('reaction_type', 'content_type', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at', 'content_object_display', 'emoji_display')
    ordering = ('-created_at',)
    
    def emoji_display(self, obj):
        return obj.get_emoji()
    emoji_display.short_description = "Emoji"
    
    def content_object_display(self, obj):
        if obj.content_object:
            return str(obj.content_object)
        return "Object not found"
    content_object_display.short_description = "Reacted Object"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content_type')
