from django.contrib import admin
from .models import Career


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'acronym', 'career_type', 'duration_display', 'faculty', 'student_count', 'is_active')
    list_filter = ('career_type', 'modality', 'faculty', 'is_active', 'requires_admission_exam')
    search_fields = ('name', 'code', 'acronym', 'faculty', 'department')
    readonly_fields = ('created_at', 'updated_at', 'student_count')
    ordering = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'acronym', 'description')
        }),
        ('Academic Details', {
            'fields': ('career_type', 'duration_years', 'duration_semesters', 'total_credits', 'modality')
        }),
        ('Organization', {
            'fields': ('faculty', 'department')
        }),
        ('Settings', {
            'fields': ('is_active', 'requires_admission_exam', 'max_students_per_semester')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_count(self, obj):
        count = obj.student_count
        return f"{count} students"
    student_count.short_description = "Active Students"
