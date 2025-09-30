from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Reaction(models.Model):
    """
    Generic reaction model for expressing different emotions
    on posts, comments, notes, etc.
    """
    
    REACTION_TYPES = [
        ('like', '👍 Like'),
        ('love', '❤️ Love'),
        ('laugh', '😂 Laugh'),
        ('wow', '😮 Wow'),
        ('sad', '😢 Sad'),
        ('angry', '😠 Angry'),
        ('celebrate', '🎉 Celebrate'),
        ('support', '💪 Support'),
    ]
    
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name="User"
    )
    
    reaction_type = models.CharField(
        max_length=15,
        choices=REACTION_TYPES,
        verbose_name="Reaction type"
    )
    
    # Generic foreign key to react to any model
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
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"
        unique_together = ['user', 'content_type', 'object_id']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['reaction_type']),
        ]
        
    def __str__(self):
        return f"{self.user.username} {self.get_reaction_type_display()} {self.content_object}"
    
    def get_emoji(self):
        """Returns the emoji for the reaction type"""
        emoji_map = {
            'like': '👍',
            'love': '❤️',
            'laugh': '😂',
            'wow': '😮',
            'sad': '😢',
            'angry': '😠',
            'celebrate': '🎉',
            'support': '💪',
        }
        return emoji_map.get(self.reaction_type, '👍')


class ReactionManager(models.Manager):
    """Custom manager for Reaction model with utility methods"""
    
    def get_reactions_for_object(self, obj):
        """Get all reactions for a specific object"""
        content_type = ContentType.objects.get_for_model(obj)
        return self.filter(
            content_type=content_type,
            object_id=obj.pk
        )
    
    def get_reaction_counts_for_object(self, obj):
        """Get reaction counts grouped by type for a specific object"""
        reactions = self.get_reactions_for_object(obj)
        counts = {}
        for reaction in reactions:
            reaction_type = reaction.reaction_type
            counts[reaction_type] = counts.get(reaction_type, 0) + 1
        return counts
    
    def get_total_reactions_for_object(self, obj):
        """Get total reaction count for a specific object"""
        return self.get_reactions_for_object(obj).count()
    
    def user_reaction_for_object(self, user, obj):
        """Get user's reaction for a specific object"""
        if not user.is_authenticated:
            return None
        content_type = ContentType.objects.get_for_model(obj)
        try:
            return self.get(
                user=user,
                content_type=content_type,
                object_id=obj.pk
            )
        except self.model.DoesNotExist:
            return None
    
    def set_reaction(self, user, obj, reaction_type):
        """Set or update user's reaction for an object"""
        content_type = ContentType.objects.get_for_model(obj)
        reaction, created = self.update_or_create(
            user=user,
            content_type=content_type,
            object_id=obj.pk,
            defaults={'reaction_type': reaction_type}
        )
        return reaction, created
    
    def remove_reaction(self, user, obj):
        """Remove user's reaction from an object"""
        content_type = ContentType.objects.get_for_model(obj)
        deleted, _ = self.filter(
            user=user,
            content_type=content_type,
            object_id=obj.pk
        ).delete()
        return deleted > 0


# Set custom manager
Reaction.objects = ReactionManager()
