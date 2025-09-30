from django.db import models
from django.urls import reverse


class Career(models.Model):
    
    CAREER_TYPES = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('technical', 'Technical'),
        ('specialization', 'Specialization'),
        ('master', 'Master'),
        ('doctorate', 'Doctorate'),
    ]
    
    MODALITIES = [
        ('presential', 'Presential'),
        ('virtual', 'Virtual'),
        ('hybrid', 'Hybrid'),
        ('distance', 'Distance'),
    ]
    
    name = models.CharField(
        max_length=200, 
        verbose_name="Career name",
        help_text="Full name of the career"
    )
    
    code = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Code",
        help_text="Unique career code (e.g.: ENG001, MED002)"
    )
    
    acronym = models.CharField(
        max_length=10, 
        blank=True, 
        verbose_name="Acronym",
        help_text="Career acronym (e.g.: CSE, MED, ENG)"
    )
    
    description = models.TextField(
        verbose_name="Description",
        help_text="Detailed career description"
    )
    
    career_type = models.CharField(
        max_length=20,
        choices=CAREER_TYPES,
        default='undergraduate',
        verbose_name="Career type"
    )
    
    duration_semesters = models.PositiveIntegerField(
        verbose_name="Duration in semesters",
        help_text="Total number of semesters for the career"
    )
    
    duration_years = models.PositiveIntegerField(
        verbose_name="Duration in years",
        help_text="Total number of years for the career"
    )
    
    total_credits = models.PositiveIntegerField(
        verbose_name="Total credits",
        help_text="Total academic credits required"
    )
    
    modality = models.CharField(
        max_length=15,
        choices=MODALITIES,
        default='presential',
        verbose_name="Modality"
    )
    
    faculty = models.CharField(
        max_length=100,
        verbose_name="Faculty",
        help_text="Faculty to which the career belongs"
    )
    
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Department",
        help_text="Specific department within the faculty"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active career",
        help_text="Whether the career is available for enrollment"
    )
    
    requires_admission_exam = models.BooleanField(
        default=False,
        verbose_name="Requires admission exam"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at"
    )
    
    max_students_per_semester = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Max students per semester",
        help_text="Maximum number of students that can enroll per semester"
    )
    
    class Meta:
        verbose_name = "Career"
        verbose_name_plural = "Careers"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_absolute_url(self):
        return reverse('career:detail', kwargs={'code': self.code})
    
    @property
    def duration_display(self):
        return f"{self.duration_years} years ({self.duration_semesters} semesters)"
    
    @property
    def student_count(self):
        return self.students.filter(is_active=True).count()
    
    def save(self, *args, **kwargs):
        if not self.acronym:
            words = self.name.split()
            self.acronym = ''.join([word[0].upper() for word in words[:3]])
        
        super().save(*args, **kwargs)