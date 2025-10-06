from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation


class Post(models.Model):
    
    POST_TYPES = [
        ('text', 'Text Only'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link'),
        ('question', 'Question'),
        ('announcement', 'Announcement'),
    ]
    
    PRIVACY_LEVELS = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('group', 'Group Only'),
        ('private', 'Private'),
    ]
    
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Author"
    )
    
    content = models.TextField(
        verbose_name="Content"
    )
    
    post_type = models.CharField(
        max_length=15,
        choices=POST_TYPES,
        default='text',
        verbose_name="Post type"
    )
    
    privacy_level = models.CharField(
        max_length=10,
        choices=PRIVACY_LEVELS,
        default='public',
        verbose_name="Privacy level"
    )
    
    image = models.ImageField(
        upload_to='posts/images/%Y/%m/',
        blank=True,
        verbose_name="Image"
    )
    
    video = models.FileField(
        upload_to='posts/videos/%Y/%m/',
        blank=True,
        verbose_name="Video"
    )
    
    link_url = models.URLField(
        blank=True,
        verbose_name="Link URL"
    )
    
    link_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Link title"
    )
    
    link_description = models.TextField(
        blank=True,
        verbose_name="Link description"
    )
    
    subject = models.ForeignKey(
        'subject.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name="Related subject"
    )
    
    group = models.ForeignKey(
        'group.Group',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name="Group"
    )
    
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags",
        verbose_name="Tags"
    )
    
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Views count"
    )
    
    is_pinned = models.BooleanField(
        default=False,
        verbose_name="Pinned"
    )
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured"
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
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['post_type', '-created_at']),
            models.Index(fields=['subject', '-created_at']),
        ]
        
    def __str__(self):
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"{self.author.username}: {content_preview}"
    
    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'pk': self.pk})
    
    def get_tags_list(self):
        """Returns tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    def get_like_count(self):
        """Get total likes for this post"""
        return self.likes.count()
    
    def get_reaction_counts(self):
        """Get reaction counts for this post"""
        from apps.reaction.models import Reaction
        return Reaction.objects.get_reaction_counts_for_object(self)
    
    def get_comment_count(self):
        """Get total comments for this post"""
        return self.comments.count()
    
    def increment_views(self):
        """Increment views count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def can_view(self, user):
        """Check if user can view this post"""
        if self.privacy_level == 'public':
            return True
        elif self.privacy_level == 'private':
            return user == self.author
        elif self.privacy_level == 'friends':
            return user == self.author or user in self.author.get_friends()
        elif self.privacy_level == 'group':
            return self.group and user in self.group.members.all()
        return False
