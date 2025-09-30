from django.contrib import admin
from .models import Note, NoteFavorite


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subject', 'note_type', 'privacy_level', 'views_count', 'downloads_count', 'is_featured', 'created_at')
    list_filter = ('note_type', 'privacy_level', 'is_featured', 'is_active', 'subject__career', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'subject__name', 'tags')
    readonly_fields = ('views_count', 'downloads_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'subject', 'note_type', 'privacy_level')
        }),
        ('Content', {
            'fields': ('content', 'tags')
        }),
        ('File Attachment', {
            'fields': ('file_attachment',),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Statistics', {
            'fields': ('views_count', 'downloads_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'subject')


@admin.register(NoteFavorite)
class NoteFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'note', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'note__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'note')
