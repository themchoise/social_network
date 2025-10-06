
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_likes', models.BooleanField(default=True)),
                ('email_comments', models.BooleanField(default=True)),
                ('email_friendships', models.BooleanField(default=True)),
                ('email_mentions', models.BooleanField(default=True)),
                ('email_achievements', models.BooleanField(default=False)),
                ('email_groups', models.BooleanField(default=True)),
                ('app_likes', models.BooleanField(default=True)),
                ('app_comments', models.BooleanField(default=True)),
                ('app_friendships', models.BooleanField(default=True)),
                ('app_mentions', models.BooleanField(default=True)),
                ('app_achievements', models.BooleanField(default=True)),
                ('app_groups', models.BooleanField(default=True)),
                ('digest_frequency', models.CharField(choices=[('immediate', 'Immediate'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('never', 'Never')], default='daily', max_length=10, verbose_name='Email digest frequency')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Notification Preference',
                'verbose_name_plural': 'Notification Preferences',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('like', 'Like Received'), ('comment', 'Comment on Post'), ('reply', 'Reply to Comment'), ('friendship_request', 'Friendship Request'), ('friendship_accepted', 'Friendship Accepted'), ('follow', 'New Follower'), ('mention', 'Mentioned in Post'), ('group_invite', 'Group Invitation'), ('group_join', 'Joined Group'), ('achievement', 'Achievement Unlocked'), ('post_featured', 'Post Featured'), ('note_shared', 'Note Shared'), ('reaction', 'Reaction Received'), ('system', 'System Notification')], max_length=20, verbose_name='Type')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('message', models.TextField(verbose_name='Message')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='Object ID')),
                ('action_url', models.URLField(blank=True, verbose_name='Action URL')),
                ('is_read', models.BooleanField(default=False, verbose_name='Read')),
                ('is_sent', models.BooleanField(default=False, verbose_name='Sent')),
                ('priority', models.CharField(choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('urgent', 'Urgent')], default='normal', max_length=10, verbose_name='Priority')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Content type')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ['-created_at'],
            },
        ),
    ]
