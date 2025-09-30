from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'author', 'post', 'parent', 'is_reply', 'is_edited', 'is_hidden', 'created_at')
    list_filter = ('is_edited', 'is_hidden', 'created_at')
    search_fields = ('content', 'author__username', 'post__content')
    readonly_fields = ('created_at', 'updated_at', 'like_count', 'replies_count')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Content', {
            'fields': ('author', 'post', 'parent', 'content')
        }),
        ('Media', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('Moderation', {
            'fields': ('is_edited', 'is_hidden')
        }),
        ('Statistics', {
            'fields': ('like_count', 'replies_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"
    
    def is_reply(self, obj):
        return obj.is_reply()
    is_reply.boolean = True
    is_reply.short_description = "Reply"
    
    def like_count(self, obj):
        return obj.get_like_count()
    like_count.short_description = "Likes"
    
    def replies_count(self, obj):
        return obj.get_replies_count()
    replies_count.short_description = "Replies"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'post', 'parent')
