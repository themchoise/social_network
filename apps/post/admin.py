from django.contrib import admin
from django.utils.html import format_html
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'author', 'post_type', 'privacy_level', 'subject', 'group', 'views_count', 'is_pinned', 'created_at')
    list_filter = ('post_type', 'privacy_level', 'is_pinned', 'is_featured', 'is_hidden', 'created_at', 'subject__career')
    search_fields = ('content', 'author__username', 'author__email', 'tags')
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'like_count', 'reaction_counts')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Content', {
            'fields': ('author', 'content', 'post_type', 'tags')
        }),
        ('Media', {
            'fields': ('image', 'video', 'link_url', 'link_title', 'link_description'),
            'classes': ('collapse',)
        }),
        ('Associations', {
            'fields': ('subject', 'group', 'privacy_level')
        }),
        ('Moderation', {
            'fields': ('is_pinned', 'is_featured', 'is_hidden')
        }),
        ('Statistics', {
            'fields': ('views_count', 'like_count', 'reaction_counts'),
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
    
    def like_count(self, obj):
        return obj.get_like_count()
    like_count.short_description = "Likes"
    
    def reaction_counts(self, obj):
        counts = obj.get_reaction_counts()
        if counts:
            return ", ".join([f"{k}: {v}" for k, v in counts.items()])
        return "No reactions"
    reaction_counts.short_description = "Reactions"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'subject', 'group')
