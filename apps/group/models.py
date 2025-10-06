from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Group(models.Model):
    
    GROUP_TYPES = [
        ('study', 'Study Group'),
        ('project', 'Project Group'),
        ('subject', 'Subject Group'),
        ('career', 'Career Group'),
        ('social', 'Social Group'),
        ('official', 'Official Group'),
    ]
    
    PRIVACY_LEVELS = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('secret', 'Secret'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name="Group name"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    creator = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='created_groups',
        verbose_name="Creator"
    )
    
    admins = models.ManyToManyField(
        'user.User',
        related_name='admin_groups',
        blank=True,
        verbose_name="Administrators"
    )
    
    members = models.ManyToManyField(
        'user.User',
        through='GroupMembership',
        related_name='user_groups',
        verbose_name="Members"
    )
    
    group_type = models.CharField(
        max_length=15,
        choices=GROUP_TYPES,
        default='study',
        verbose_name="Group type"
    )
    
    privacy_level = models.CharField(
        max_length=10,
        choices=PRIVACY_LEVELS,
        default='public',
        verbose_name="Privacy level"
    )
    
    subject = models.ForeignKey(
        'subject.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='groups',
        verbose_name="Related subject"
    )
    
    career = models.ForeignKey(
        'career.Career',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='groups',
        verbose_name="Related career"
    )
    
    max_members = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(2), MaxValueValidator(1000)],
        verbose_name="Maximum members"
    )
    
    allow_member_posts = models.BooleanField(
        default=True,
        verbose_name="Allow member posts"
    )
    
    require_approval = models.BooleanField(
        default=False,
        verbose_name="Require approval to join"
    )
    
    avatar = models.ImageField(
        upload_to='groups/avatars/%Y/%m/',
        blank=True,
        verbose_name="Group avatar"
    )
    
    banner = models.ImageField(
        upload_to='groups/banners/%Y/%m/',
        blank=True,
        verbose_name="Group banner"
    )
    
    rules = models.TextField(
        blank=True,
        verbose_name="Group rules"
    )
    
    total_posts = models.PositiveIntegerField(
        default=0,
        verbose_name="Total posts"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
    )
    
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('group:detail', kwargs={'pk': self.pk})
    
    def get_member_count(self):
        """Get total number of members"""
        return self.members.count()
    
    def is_admin(self, user):
        """Check if user is admin of this group"""
        return user == self.creator or user in self.admins.all()
    
    def is_member(self, user):
        """Check if user is member of this group"""
        return user in self.members.all()
    
    def can_user_join(self, user):
        """Check if user can join this group"""
        if self.is_member(user):
            return False
        if self.max_members and self.get_member_count() >= self.max_members:
            return False
        return True
    
    def can_user_post(self, user):
        """Check if user can post in this group"""
        if not self.is_member(user):
            return False
        if not self.allow_member_posts and not self.is_admin(user):
            return False
        return True
    
    def increment_posts(self):
        """Increment total posts count"""
        self.total_posts += 1
        self.save(update_fields=['total_posts'])


class GroupMembership(models.Model):
    """Intermediate model for group membership with additional data"""
    
    MEMBERSHIP_ROLES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Administrator'),
    ]
    
    MEMBERSHIP_STATUS = [
        ('active', 'Active'),
        ('pending', 'Pending Approval'),
        ('banned', 'Banned'),
        ('left', 'Left Group'),
    ]
    
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name="User"
    )
    
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name="Group"
    )
    
    role = models.CharField(
        max_length=15,
        choices=MEMBERSHIP_ROLES,
        default='member',
        verbose_name="Role"
    )
    
    status = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_STATUS,
        default='active',
        verbose_name="Status"
    )
    
    joined_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    # Notification preferences
    notify_posts = models.BooleanField(
        default=True,
        verbose_name="Notify on new posts"
    )
    
    notify_events = models.BooleanField(
        default=True,
        verbose_name="Notify on events"
    )
    
    class Meta:
        unique_together = ['user', 'group']
        verbose_name = "Group Membership"
        verbose_name_plural = "Group Memberships"
        ordering = ['-joined_at']
        
    def __str__(self):
        return f"{self.user.username} in {self.group.name} ({self.role})"
