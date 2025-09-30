from django.contrib import admin
from .models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'achievement_type', 'level', 'points', 'is_active', 'created_at')
    list_filter = ('achievement_type', 'level', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'condition_description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('achievement_type', 'level', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'achievement_type', 'level')
        }),
        ('Rewards', {
            'fields': ('points', 'icon')
        }),
        ('Conditions', {
            'fields': ('condition_description',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'progress', 'earned_at')
    list_filter = ('achievement__achievement_type', 'achievement__level', 'earned_at')
    search_fields = ('user__username', 'achievement__name')
    readonly_fields = ('earned_at',)
    ordering = ('-earned_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'achievement')
