from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation


class Comment(models.Model):
    
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Author"
    )
    
    post = models.ForeignKey(
        'post.Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Post"
    )
    
    content = models.TextField(
        verbose_name="Content"
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="Parent comment"
    )
    
    image = models.ImageField(
        upload_to='comments/images/%Y/%m/',
        blank=True,
        verbose_name="Image"
    )
    
    is_edited = models.BooleanField(
        default=False,
        verbose_name="Edited"
    )
    
    is_hidden = models.BooleanField(
        default=False,
        verbose_name="Hidden"
    )
    
    likes = GenericRelation('like.Like')
    reactions = GenericRelation('reaction.Reaction')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['parent']),
        ]
        
    def __str__(self):
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"{self.author.username}: {content_preview}"
    
    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.pk}"
    
    def get_like_count(self):
        """Get total likes for this comment"""
        return self.likes.count()
    
    def get_reaction_counts(self):
        """Get reaction counts for this comment"""
        from apps.reaction.models import Reaction
        return Reaction.objects.get_reaction_counts_for_object(self)
    
    def get_replies_count(self):
        """Get total replies for this comment"""
        return self.replies.count()
    
    def is_reply(self):
        """Check if this comment is a reply to another comment"""
        return self.parent is not None
    
    def get_thread_comments(self):
        """Get all comments in the same thread (for nested comments)"""
        if self.parent:
            return self.parent.replies.all()
        return self.replies.all()
    
    def mark_as_edited(self):
        """Mark comment as edited"""
        self.is_edited = True
        self.save(update_fields=['is_edited', 'updated_at'])
