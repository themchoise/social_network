
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Group name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('group_type', models.CharField(choices=[('study', 'Study Group'), ('project', 'Project Group'), ('subject', 'Subject Group'), ('career', 'Career Group'), ('social', 'Social Group'), ('official', 'Official Group')], default='study', max_length=15, verbose_name='Group type')),
                ('privacy_level', models.CharField(choices=[('public', 'Public'), ('private', 'Private'), ('secret', 'Secret')], default='public', max_length=10, verbose_name='Privacy level')),
                ('max_members', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(1000)], verbose_name='Maximum members')),
                ('allow_member_posts', models.BooleanField(default=True, verbose_name='Allow member posts')),
                ('require_approval', models.BooleanField(default=False, verbose_name='Require approval to join')),
                ('avatar', models.ImageField(blank=True, upload_to='groups/avatars/%Y/%m/', verbose_name='Group avatar')),
                ('banner', models.ImageField(blank=True, upload_to='groups/banners/%Y/%m/', verbose_name='Group banner')),
                ('rules', models.TextField(blank=True, verbose_name='Group rules')),
                ('total_posts', models.PositiveIntegerField(default=0, verbose_name='Total posts')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('member', 'Member'), ('moderator', 'Moderator'), ('admin', 'Administrator')], default='member', max_length=15, verbose_name='Role')),
                ('status', models.CharField(choices=[('active', 'Active'), ('pending', 'Pending Approval'), ('banned', 'Banned'), ('left', 'Left Group')], default='active', max_length=10, verbose_name='Status')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('notify_posts', models.BooleanField(default=True, verbose_name='Notify on new posts')),
                ('notify_events', models.BooleanField(default=True, verbose_name='Notify on events')),
            ],
            options={
                'verbose_name': 'Group Membership',
                'verbose_name_plural': 'Group Memberships',
                'ordering': ['-joined_at'],
            },
        ),
    ]
