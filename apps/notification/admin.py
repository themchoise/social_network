from django.contrib import admin
from .models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'sender', 'notification_type', 'priority', 'is_read', 'is_sent', 'created_at')
    list_filter = ('notification_type', 'priority', 'is_read', 'is_sent', 'created_at')
    search_fields = ('title', 'message', 'recipient__username', 'sender__username')
    readonly_fields = ('created_at', 'read_at', 'sent_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Recipients', {
            'fields': ('recipient', 'sender')
        }),
        ('Content', {
            'fields': ('notification_type', 'title', 'message', 'priority')
        }),
        ('Action', {
            'fields': ('action_url',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'is_sent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at', 'sent_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_sent']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_sent(self, request, queryset):
        queryset.update(is_sent=True)
    mark_as_sent.short_description = "Mark selected notifications as sent"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('recipient', 'sender')


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'app_notifications', 'digest_frequency', 'updated_at')
    list_filter = ('digest_frequency', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Email Notifications', {
            'fields': ('email_likes', 'email_comments', 'email_friendships', 'email_mentions', 'email_achievements', 'email_groups')
        }),
        ('App Notifications', {
            'fields': ('app_likes', 'app_comments', 'app_friendships', 'app_mentions', 'app_achievements', 'app_groups')
        }),
        ('Settings', {
            'fields': ('digest_frequency',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def email_notifications(self, obj):
        enabled = sum([obj.email_likes, obj.email_comments, obj.email_friendships, 
                      obj.email_mentions, obj.email_achievements, obj.email_groups])
        return f"{enabled}/6 enabled"
    email_notifications.short_description = "Email"
    
    def app_notifications(self, obj):
        enabled = sum([obj.app_likes, obj.app_comments, obj.app_friendships, 
                      obj.app_mentions, obj.app_achievements, obj.app_groups])
        return f"{enabled}/6 enabled"
    app_notifications.short_description = "In-App"
