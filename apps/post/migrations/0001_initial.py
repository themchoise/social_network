
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('post_type', models.CharField(choices=[('text', 'Text Only'), ('image', 'Image'), ('video', 'Video'), ('link', 'Link'), ('question', 'Question'), ('announcement', 'Announcement')], default='text', max_length=15, verbose_name='Post type')),
                ('privacy_level', models.CharField(choices=[('public', 'Public'), ('friends', 'Friends Only'), ('group', 'Group Only'), ('private', 'Private')], default='public', max_length=10, verbose_name='Privacy level')),
                ('image', models.ImageField(blank=True, upload_to='posts/images/%Y/%m/', verbose_name='Image')),
                ('video', models.FileField(blank=True, upload_to='posts/videos/%Y/%m/', verbose_name='Video')),
                ('link_url', models.URLField(blank=True, verbose_name='Link URL')),
                ('link_title', models.CharField(blank=True, max_length=200, verbose_name='Link title')),
                ('link_description', models.TextField(blank=True, verbose_name='Link description')),
                ('tags', models.CharField(blank=True, help_text='Comma-separated tags', max_length=500, verbose_name='Tags')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Views count')),
                ('is_pinned', models.BooleanField(default=False, verbose_name='Pinned')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-created_at'],
            },
        ),
    ]
