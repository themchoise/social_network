from django.db import models
from django.urls import reverse


class Subject(models.Model):
    
    SUBJECT_TYPES = [
        ('mandatory', 'Mandatory'),
        ('elective', 'Elective'),
        ('optional', 'Optional'),
    ]
    
    name = models.CharField(
        max_length=200, 
        verbose_name="Subject name"
    )
    
    code = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Subject code"
    )
    
    career = models.ForeignKey(
        'career.Career',
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name="Career"
    )
    
    semester = models.PositiveIntegerField(
        verbose_name="Semester"
    )
    
    credits = models.PositiveIntegerField(
        verbose_name="Credits"
    )
    
    subject_type = models.CharField(
        max_length=15,
        choices=SUBJECT_TYPES,
        default='mandatory',
        verbose_name="Subject type"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    prerequisites = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='unlocks',
        verbose_name="Prerequisites"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ['career', 'semester', 'name']
        unique_together = ['career', 'code']
        
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_absolute_url(self):
        return reverse('subject:detail', kwargs={'code': self.code})
