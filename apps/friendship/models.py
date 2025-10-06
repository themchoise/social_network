from django.db import models
from django.urls import reverse


class Friendship(models.Model):
    
    FRIENDSHIP_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('blocked', 'Blocked'),
    ]
    
    sender = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='sent_friendships',
        verbose_name="Sender"
    )
    
    receiver = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='received_friendships',
        verbose_name="Receiver"
    )
    
    status = models.CharField(
        max_length=10,
        choices=FRIENDSHIP_STATUS,
        default='pending',
        verbose_name="Status"
    )
    
    request_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Request date"
    )
    
    response_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Response date"
    )
    
    message = models.TextField(
        blank=True,
        max_length=200,
        verbose_name="Request message"
    )
    
    class Meta:
        unique_together = ('sender', 'receiver')
        verbose_name = "Friendship"
        verbose_name_plural = "Friendships"
        ordering = ['-request_date']
        
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"
    
    def accept(self):
        """Accept friendship request"""
        self.status = 'accepted'
        self.response_date = models.timezone.now()
        self.save()
        
        # Award points to both users
        self.sender.add_points(10)  # Points for sending request
        self.receiver.add_points(5)  # Points for accepting
    
    def reject(self):
        """Reject friendship request"""
        self.status = 'rejected'
        self.response_date = models.timezone.now()
        self.save()
    
    def block(self):
        """Block user"""
        self.status = 'blocked'
        self.response_date = models.timezone.now()
        self.save()
    
    @classmethod
    def are_friends(cls, user1, user2):
        """Check if two users are friends"""
        return cls.objects.filter(
            models.Q(sender=user1, receiver=user2, status='accepted') |
            models.Q(sender=user2, receiver=user1, status='accepted')
        ).exists()
    
    @classmethod
    def get_friendship_status(cls, user1, user2):
        """Get friendship status between two users"""
        try:
            friendship = cls.objects.get(
                models.Q(sender=user1, receiver=user2) |
                models.Q(sender=user2, receiver=user1)
            )
            return friendship.status
        except cls.DoesNotExist:
            return None


class Follow(models.Model):
    """Follow system for users to follow each other without mutual acceptance"""
    
    follower = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name="Follower"
    )
    
    followed = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name="Followed"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    notify_posts = models.BooleanField(
        default=True,
        verbose_name="Notify on posts"
    )
    
    notify_achievements = models.BooleanField(
        default=True,
        verbose_name="Notify on achievements"
    )
    
    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
    
    def save(self, *args, **kwargs):
        if self.follower == self.followed:
            raise ValueError("Users cannot follow themselves")
        super().save(*args, **kwargs)


class Block(models.Model):
    """Block system for users to block each other"""
    
    blocker = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='blocked_users',
        verbose_name="Blocker"
    )
    
    blocked = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='blocked_by',
        verbose_name="Blocked"
    )
    
    reason = models.TextField(
        blank=True,
        verbose_name="Reason"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('blocker', 'blocked')
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"
    
    def save(self, *args, **kwargs):
        # Prevent self-blocking
        if self.blocker == self.blocked:
            raise ValueError("Users cannot block themselves")
        super().save(*args, **kwargs)
