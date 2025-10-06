
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, verbose_name='Reason')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Block',
                'verbose_name_plural': 'Blocks',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notify_posts', models.BooleanField(default=True, verbose_name='Notify on posts')),
                ('notify_achievements', models.BooleanField(default=True, verbose_name='Notify on achievements')),
            ],
            options={
                'verbose_name': 'Follow',
                'verbose_name_plural': 'Follows',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('blocked', 'Blocked')], default='pending', max_length=10, verbose_name='Status')),
                ('request_date', models.DateTimeField(auto_now_add=True, verbose_name='Request date')),
                ('response_date', models.DateTimeField(blank=True, null=True, verbose_name='Response date')),
                ('message', models.TextField(blank=True, max_length=200, verbose_name='Request message')),
            ],
            options={
                'verbose_name': 'Friendship',
                'verbose_name_plural': 'Friendships',
                'ordering': ['-request_date'],
            },
        ),
    ]
