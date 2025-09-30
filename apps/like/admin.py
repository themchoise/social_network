from django.contrib import admin
from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'content_object_display', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'content_object_display')
    ordering = ('-created_at',)
    
    def content_object_display(self, obj):
        if obj.content_object:
            return str(obj.content_object)
        return "Object not found"
    content_object_display.short_description = "Liked Object"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'content_type')
