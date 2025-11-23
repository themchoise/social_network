"""
Admin mejorado para gestionar logros y ver estadísticas de puntos.

Copiar el contenido de este archivo a apps/achievement/admin.py
"""

from django.contrib import admin
from django.utils.html import format_html
from apps.achievement.models import Achievement, UserAchievement
from apps.user.models import User, UserPointsHistory


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'achievement_type', 'level_badge', 'points', 'is_active', 'user_count']
    list_filter = ['achievement_type', 'level', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description', 'achievement_type')
        }),
        ('Detalles', {
            'fields': ('level', 'points', 'icon', 'is_active')
        }),
        ('Condiciones', {
            'fields': ('condition_description',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def level_badge(self, obj):
        colors = {
            'bronze': '#CD7F32',
            'silver': '#C0C0C0',
            'gold': '#FFD700',
            'platinum': '#E5E4E2',
        }
        color = colors.get(obj.level, '#999')
        return format_html(
            '<span style="background-color: {}; color: black; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_level_display()
        )
    level_badge.short_description = 'Nivel'
    
    def user_count(self, obj):
        count = obj.user_achievements.count()
        return format_html(
            '<span style="background-color: #e3f2fd; padding: 2px 6px; border-radius: 3px;">{} usuarios</span>',
            count
        )
    user_count.short_description = 'Usuarios'


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['achievement_name', 'user_link', 'earned_at_short']
    list_filter = ['achievement__achievement_type', 'earned_at']
    search_fields = ['user__username', 'achievement__name']
    readonly_fields = ['earned_at', 'user_info', 'achievement_info']
    
    fieldsets = (
        ('Usuario y Logro', {
            'fields': ('user_link', 'achievement_name')
        }),
        ('Información Detallada', {
            'fields': ('user_info', 'achievement_info'),
            'classes': ('collapse',)
        }),
        ('Fecha', {
            'fields': ('earned_at',)
        }),
    )
    
    def achievement_name(self, obj):
        return obj.achievement.name
    achievement_name.short_description = 'Logro'
    
    def user_link(self, obj):
        return format_html(
            '<a href="/admin/user/user/{}/change/">{}</a>',
            obj.user.id, obj.user.username
        )
    user_link.short_description = 'Usuario'
    
    def earned_at_short(self, obj):
        return obj.earned_at.strftime('%d/%m/%Y %H:%M')
    earned_at_short.short_description = 'Desbloqueado'
    
    def user_info(self, obj):
        return f"{obj.user.username} (Nivel {obj.user.level}, {obj.user.total_points} pts)"
    user_info.short_description = 'Información del Usuario'
    
    def achievement_info(self, obj):
        return f"{obj.achievement.name} - {obj.achievement.get_level_display()} ({obj.achievement.points} pts)"
    achievement_info.short_description = 'Información del Logro'


@admin.register(UserPointsHistory)
class UserPointsHistoryAdmin(admin.ModelAdmin):
    list_display = ['user_link', 'points_display', 'source_display', 'created_at_short']
    list_filter = ['source', 'created_at']
    search_fields = ['user__username', 'description']
    readonly_fields = ['user', 'points', 'source', 'description', 'created_at', 'user_stats']
    
    fieldsets = (
        ('Información de Puntos', {
            'fields': ('user_link', 'points_display', 'source_display', 'description')
        }),
        ('Estadísticas del Usuario', {
            'fields': ('user_stats',),
            'classes': ('collapse',)
        }),
        ('Fecha', {
            'fields': ('created_at',)
        }),
    )
    
    can_add = False
    can_delete = False
    
    def user_link(self, obj):
        return format_html(
            '<a href="/admin/user/user/{}/change/">{}</a>',
            obj.user.id, obj.user.username
        )
    user_link.short_description = 'Usuario'
    
    def points_display(self, obj):
        color = '#4caf50' if obj.points > 0 else '#f44336'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold;">+{}</span>',
            color, obj.points
        )
    points_display.short_description = 'Puntos'
    
    def source_display(self, obj):
        colors = {
            'post': '#2196F3',
            'comment': '#4CAF50',
            'like_received': '#FF5252',
            'note_shared': '#FF9800',
            'achievement': '#9C27B0',
            'login_streak': '#00BCD4',
            'help_others': '#8BC34A',
            'admin_bonus': '#FFC107',
        }
        color = colors.get(obj.source, '#999')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_source_display()
        )
    source_display.short_description = 'Fuente'
    
    def created_at_short(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    created_at_short.short_description = 'Fecha'
    
    def user_stats(self, obj):
        user = obj.user
        return f"""
        Nivel: {user.level}
        Puntos Totales: {user.total_points}
        Experiencia: {user.experience_points}
        Posts: {user.posts.count()}
        Logros: {user.user_achievements.count()}
        """
    user_stats.short_description = 'Estadísticas'
    
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
