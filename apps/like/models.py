from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class LikeManager(models.Manager):
    """Custom manager for Like model with utility methods"""
    
    def get_likes_for_object(self, obj):
        """Get all likes for a specific object"""
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(
            content_type=content_type,
            object_id=obj.pk
        )
    
    def get_like_count_for_object(self, obj):
        """Get like count for a specific object"""
        return self.get_likes_for_object(obj).count()
    
    def user_has_liked(self, user, obj):
        """Check if user has liked a specific object"""
        if not user.is_authenticated:
            return False
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(
            user=user,
            content_type=content_type,
            object_id=obj.pk
        ).exists()
    
    def toggle_like(self, user, obj):
        """Toggle like for user on object. Returns (like_instance, created)"""
        content_type = ContentType.objects.get_for_model(obj)
        like, created = self.get_or_create(
            user=user,
            content_type=content_type,
            object_id=obj.pk
        )
        if not created:
            like.delete()
            return None, False
        return like, True


class Like(models.Model):
    """
    Generic like model that can be applied to any content type
    (Posts, Comments, Notes, etc.)
    """
    
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="User"
    )
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name="Content type"
    )
    
    object_id = models.PositiveIntegerField(
        verbose_name="Object ID"
    )
    
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = LikeManager()
    
    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user', 'created_at']),
        ]
        
    def __str__(self):
        return f"{self.user.username} likes {self.content_object}"
