from django.contrib import admin
from .models import Group, GroupMembership


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0
    readonly_fields = ('joined_at', 'last_activity')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'group_type', 'privacy_level', 'member_count_display', 'total_posts', 'is_active', 'created_at')
    list_filter = ('group_type', 'privacy_level', 'is_active', 'is_featured', 'subject__career', 'created_at')
    search_fields = ('name', 'description', 'creator__username', 'subject__name', 'career__name')
    readonly_fields = ('total_posts', 'created_at', 'updated_at', 'member_count_display')
    ordering = ('-created_at',)
    inlines = [GroupMembershipInline]
    filter_horizontal = ('admins',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'creator', 'group_type', 'privacy_level')
        }),
        ('Academic Relations', {
            'fields': ('subject', 'career'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('max_members', 'allow_member_posts', 'require_approval')
        }),
        ('Media', {
            'fields': ('avatar', 'banner'),
            'classes': ('collapse',)
        }),
        ('Rules', {
            'fields': ('rules',),
            'classes': ('collapse',)
        }),
        ('Administration', {
            'fields': ('admins', 'is_active', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('total_posts', 'member_count_display'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def member_count_display(self, obj):
        return f"{obj.get_member_count()} members"
    member_count_display.short_description = "Members"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('creator', 'subject', 'career')


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'status', 'joined_at', 'last_activity')
    list_filter = ('role', 'status', 'joined_at', 'notify_posts', 'notify_events')
    search_fields = ('user__username', 'group__name')
    readonly_fields = ('joined_at', 'last_activity')
    ordering = ('-joined_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'group')
