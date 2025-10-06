
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('group', '0002_initial'),
        ('post', '0001_initial'),
        ('subject', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='group.group', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='post',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='subject.subject', verbose_name='Related subject'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author', '-created_at'], name='post_post_author__cd6e37_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['post_type', '-created_at'], name='post_post_post_ty_4ec4d9_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['subject', '-created_at'], name='post_post_subject_83304a_idx'),
        ),
    ]
