
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reaction', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddIndex(
            model_name='reaction',
            index=models.Index(fields=['content_type', 'object_id'], name='reaction_re_content_08fb7b_idx'),
        ),
        migrations.AddIndex(
            model_name='reaction',
            index=models.Index(fields=['user', 'created_at'], name='reaction_re_user_id_e76f80_idx'),
        ),
        migrations.AddIndex(
            model_name='reaction',
            index=models.Index(fields=['reaction_type'], name='reaction_re_reactio_83a9bd_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together={('user', 'content_type', 'object_id')},
        ),
    ]
