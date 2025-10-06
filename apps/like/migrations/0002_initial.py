
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('like', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddIndex(
            model_name='like',
            index=models.Index(fields=['content_type', 'object_id'], name='like_like_content_07edaa_idx'),
        ),
        migrations.AddIndex(
            model_name='like',
            index=models.Index(fields=['user', 'created_at'], name='like_like_user_id_19835b_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'content_type', 'object_id')},
        ),
    ]
