from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


class Notification(models.Model):
    
    NOTIFICATION_TYPES = [
        ('like', 'Like Received'),
        ('comment', 'Comment on Post'),
        ('reply', 'Reply to Comment'),
        ('friendship_request', 'Friendship Request'),
        ('friendship_accepted', 'Friendship Accepted'),
        ('follow', 'New Follower'),
        ('mention', 'Mentioned in Post'),
        ('group_invite', 'Group Invitation'),
        ('group_join', 'Joined Group'),
        ('achievement', 'Achievement Unlocked'),
        ('post_featured', 'Post Featured'),
        ('note_shared', 'Note Shared'),
        ('reaction', 'Reaction Received'),
        ('system', 'System Notification'),
    ]
    
    recipient = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name="Recipient"
    )
    
    sender = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name="Sender"
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name="Type"
    )
    
    title = models.CharField(
        max_length=100,
        verbose_name="Title"
    )
    
    message = models.TextField(
        verbose_name="Message"
    )
    
    # Generic relation to any object
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Content type"
    )
    
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Object ID"
    )
    
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Action URL (optional override for custom URLs)
    action_url = models.URLField(
        blank=True,
        verbose_name="Action URL"
    )
    
    # Status
    is_read = models.BooleanField(
        default=False,
        verbose_name="Read"
    )
    
    is_sent = models.BooleanField(
        default=False,
        verbose_name="Sent"
    )
    
    # Priority
    priority = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        default='normal',
        verbose_name="Priority"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['is_read', '-created_at']),
            models.Index(fields=['notification_type']),
        ]
        
    def __str__(self):
        return f"{self.title} for {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = models.timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def get_action_url(self):
        """Get the action URL for this notification"""
        if self.action_url:
            return self.action_url
        elif self.content_object and hasattr(self.content_object, 'get_absolute_url'):
            return self.content_object.get_absolute_url()
        return '#'
    
    def get_icon_class(self):
        """Get icon class based on notification type"""
        icon_map = {
            'like': 'fa-heart',
            'comment': 'fa-comment',
            'reply': 'fa-reply',
            'friendship_request': 'fa-user-plus',
            'friendship_accepted': 'fa-handshake',
            'follow': 'fa-user-check',
            'mention': 'fa-at',
            'group_invite': 'fa-users',
            'group_join': 'fa-user-friends',
            'achievement': 'fa-trophy',
            'post_featured': 'fa-star',
            'note_shared': 'fa-file-alt',
            'reaction': 'fa-smile',
            'system': 'fa-info-circle',
        }
        return icon_map.get(self.notification_type, 'fa-bell')
    
    @classmethod
    def create_notification(cls, recipient, notification_type, title, message, 
                          sender=None, content_object=None, action_url=None, priority='normal'):
        """Helper method to create notifications"""
        notification = cls.objects.create(
            recipient=recipient,
            sender=sender,
            notification_type=notification_type,
            title=title,
            message=message,
            content_object=content_object,
            action_url=action_url,
            priority=priority
        )
        return notification


class NotificationPreference(models.Model):
    """User preferences for notifications"""
    
    user = models.OneToOneField(
        'user.User',
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name="User"
    )
    
    # Email notifications
    email_likes = models.BooleanField(default=True)
    email_comments = models.BooleanField(default=True)
    email_friendships = models.BooleanField(default=True)
    email_mentions = models.BooleanField(default=True)
    email_achievements = models.BooleanField(default=False)
    email_groups = models.BooleanField(default=True)
    
    # In-app notifications
    app_likes = models.BooleanField(default=True)
    app_comments = models.BooleanField(default=True)
    app_friendships = models.BooleanField(default=True)
    app_mentions = models.BooleanField(default=True)
    app_achievements = models.BooleanField(default=True)
    app_groups = models.BooleanField(default=True)
    
    # Frequency settings
    digest_frequency = models.CharField(
        max_length=10,
        choices=[
            ('immediate', 'Immediate'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('never', 'Never'),
        ],
        default='daily',
        verbose_name="Email digest frequency"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Notification Preference"
        verbose_name_plural = "Notification Preferences"
        
    def __str__(self):
        return f"Preferences for {self.user.username}"
