from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MinValueValidator


class User(AbstractUser):
    
    email = models.EmailField(
        unique=True,
        verbose_name="Email address"
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Biography"
    )
    
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        blank=True,
        verbose_name="Avatar"
    )
    
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Birth date"
    )
    
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Location"
    )
    
    website = models.URLField(
        blank=True,
        verbose_name="Website"
    )
    
    career = models.ForeignKey(
        'career.Career',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name="Career"
    )
    
    student_id = models.CharField(
        max_length=20,
        blank=True,
        unique=True,
        verbose_name="Student ID"
    )
    
    enrollment_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Enrollment year"
    )
    
    current_semester = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Current semester"
    )
    
    total_points = models.PositiveIntegerField(
        default=0,
        verbose_name="Total points"
    )
    
    level = models.PositiveIntegerField(
        default=1,
        verbose_name="User level"
    )
    
    experience_points = models.PositiveIntegerField(
        default=0,
        verbose_name="Experience points"
    )
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verified account"
    )
    
    is_mentor = models.BooleanField(
        default=False,
        verbose_name="Is mentor"
    )
    
    profile_visibility = models.CharField(
        max_length=10,
        choices=[
            ('public', 'Public'),
            ('friends', 'Friends Only'),
            ('private', 'Private'),
        ],
        default='public',
        verbose_name="Profile visibility"
    )
    
    show_email = models.BooleanField(
        default=False,
        verbose_name="Show email publicly"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('user:profile', kwargs={'username': self.username})
    
    def get_full_name_or_username(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username
    
    def add_points(self, points):
        self.total_points += points
        self.experience_points += points
        self.update_level()
        self.save(update_fields=['total_points', 'experience_points', 'level'])
    
    def update_level(self):
        new_level = (self.experience_points // 1000) + 1
        if new_level != self.level:
            self.level = new_level
            return True
        return False
    
    def get_achievements(self):
        return self.user_achievements.select_related('achievement')
    
    def get_friends(self):
        return User.objects.filter(
            models.Q(sent_friendships__receiver=self, sent_friendships__status='accepted') |
            models.Q(received_friendships__sender=self, received_friendships__status='accepted')
        ).distinct()
    
    def get_friend_count(self):
        return self.get_friends().count()
    
    def can_view_profile(self, viewer):
        if self.profile_visibility == 'public':
            return True
        elif self.profile_visibility == 'private':
            return viewer == self
        elif self.profile_visibility == 'friends':
            return viewer == self or viewer in self.get_friends()
        return False


class UserPointsHistory(models.Model):
    
    POINT_SOURCES = [
        ('post', 'Created Post'),
        ('comment', 'Created Comment'),
        ('like_received', 'Received Like'),
        ('note_shared', 'Shared Note'),
        ('achievement', 'Achievement Unlocked'),
        ('login_streak', 'Login Streak'),
        ('help_others', 'Helped Others'),
        ('admin_bonus', 'Admin Bonus'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='points_history',
        verbose_name="User"
    )
    
    points = models.IntegerField(
        verbose_name="Points"
    )
    
    source = models.CharField(
        max_length=20,
        choices=POINT_SOURCES,
        verbose_name="Source"
    )
    
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Description"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Points History"
        verbose_name_plural = "Points History"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username}: {self.points} points ({self.source})"

