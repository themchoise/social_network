from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'career', 'semester', 'credits', 'subject_type', 'is_active')
    list_filter = ('career', 'semester', 'subject_type', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'career__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('career', 'semester', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'career', 'description')
        }),
        ('Academic Details', {
            'fields': ('semester', 'credits', 'subject_type')
        }),
        ('Prerequisites', {
            'fields': ('prerequisites',)
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ('prerequisites',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('career')
