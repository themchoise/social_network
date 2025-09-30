from django.contrib import admin
from .models import Friendship, Follow, Block


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'request_date', 'response_date')
    list_filter = ('status', 'request_date', 'response_date')
    search_fields = ('sender__username', 'receiver__username')
    readonly_fields = ('request_date', 'response_date')
    ordering = ('-request_date',)
    
    fieldsets = (
        ('Users', {
            'fields': ('sender', 'receiver')
        }),
        ('Status', {
            'fields': ('status', 'message')
        }),
        ('Timestamps', {
            'fields': ('request_date', 'response_date'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sender', 'receiver')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'notify_posts', 'notify_achievements', 'created_at')
    list_filter = ('notify_posts', 'notify_achievements', 'created_at')
    search_fields = ('follower__username', 'followed__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('follower', 'followed')


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('blocker', 'blocked', 'reason_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('blocker__username', 'blocked__username', 'reason')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def reason_preview(self, obj):
        if obj.reason:
            return obj.reason[:50] + "..." if len(obj.reason) > 50 else obj.reason
        return "No reason provided"
    reason_preview.short_description = "Reason"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('blocker', 'blocked')
