from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserPointsHistory


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'career', 'total_points', 'level', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'career', 'is_verified', 'is_mentor', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'student_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_activity')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('bio', 'avatar', 'birth_date', 'location', 'website')
        }),
        ('Academic Information', {
            'fields': ('career', 'student_id', 'enrollment_year', 'current_semester')
        }),
        ('Gamification', {
            'fields': ('total_points', 'level', 'experience_points')
        }),
        ('Social Features', {
            'fields': ('is_verified', 'is_mentor', 'profile_visibility', 'show_email')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_activity'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('career')


@admin.register(UserPointsHistory)
class UserPointsHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'source', 'description', 'created_at')
    list_filter = ('source', 'created_at')
    search_fields = ('user__username', 'user__email', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
