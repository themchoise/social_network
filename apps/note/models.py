from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class Note(models.Model):
    
    NOTE_TYPES = [
        ('class', 'Class Notes'),
        ('summary', 'Summary'),
        ('exercise', 'Exercise'),
        ('project', 'Project'),
        ('exam', 'Exam Material'),
        ('reference', 'Reference'),
    ]
    
    PRIVACY_LEVELS = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]
    
    title = models.CharField(
        max_length=200, 
        verbose_name="Title"
    )
    
    content = models.TextField(
        verbose_name="Content"
    )
    
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name="Author"
    )
    
    subject = models.ForeignKey(
        'subject.Subject',
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name="Subject"
    )
    
    note_type = models.CharField(
        max_length=15,
        choices=NOTE_TYPES,
        default='class',
        verbose_name="Note type"
    )
    
    privacy_level = models.CharField(
        max_length=10,
        choices=PRIVACY_LEVELS,
        default='public',
        verbose_name="Privacy level"
    )
    
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags",
        verbose_name="Tags"
    )
    
    file_attachment = models.FileField(
        upload_to='notes/attachments/%Y/%m/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpg', 'png'])],
        verbose_name="File attachment"
    )
    
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Views count"
    )
    
    downloads_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Downloads count"
    )
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    def get_absolute_url(self):
        return reverse('note:detail', kwargs={'pk': self.pk})
    
    def get_tags_list(self):
        """Returns tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def increment_views(self):
        """Increment views count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_downloads(self):
        """Increment downloads count"""
        self.downloads_count += 1
        self.save(update_fields=['downloads_count'])


class NoteFavorite(models.Model):
    """Favorite notes by users"""
    
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='favorite_notes',
        verbose_name="User"
    )
    
    note = models.ForeignKey(
        Note,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name="Note"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Note Favorite"
        verbose_name_plural = "Note Favorites"
        unique_together = ['user', 'note']
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.note.title}"
