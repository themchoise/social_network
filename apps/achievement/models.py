from django.db import models
from django.urls import reverse


class Achievement(models.Model):
    
    ACHIEVEMENT_TYPES = [
        ('academic', 'Academic'),
        ('social', 'Social'),
        ('completion', 'Completion'),
        ('milestone', 'Milestone'),
        ('special', 'Special'),
    ]
    
    ACHIEVEMENT_LEVELS = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    name = models.CharField(
        max_length=200, 
        verbose_name="Achievement name"
    )
    
    description = models.TextField(
        verbose_name="Description"
    )
    
    achievement_type = models.CharField(
        max_length=15,
        choices=ACHIEVEMENT_TYPES,
        verbose_name="Achievement type"
    )
    
    level = models.CharField(
        max_length=10,
        choices=ACHIEVEMENT_LEVELS,
        default='bronze',
        verbose_name="Level"
    )
    
    points = models.PositiveIntegerField(
        default=10,
        verbose_name="Points awarded"
    )
    
    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Icon class"
    )
    
    condition_description = models.TextField(
        help_text="Description of how to unlock this achievement",
        verbose_name="Unlock condition"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        ordering = ['achievement_type', 'level', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.level})"
    
    def get_absolute_url(self):
        return reverse('achievement:detail', kwargs={'pk': self.pk})


class UserAchievement(models.Model):
    """Intermediate model for user achievements"""
    
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_achievements',
        verbose_name="User"
    )
    
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name='user_achievements',
        verbose_name="Achievement"
    )
    
    earned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Earned at"
    )
    
    progress = models.PositiveIntegerField(
        default=100,
        help_text="Progress percentage (0-100)",
        verbose_name="Progress"
    )
    
    class Meta:
        verbose_name = "User Achievement"
        verbose_name_plural = "User Achievements"
        unique_together = ['user', 'achievement']
        ordering = ['-earned_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
