
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction_type', models.CharField(choices=[('like', '👍 Like'), ('love', '❤️ Love'), ('laugh', '😂 Laugh'), ('wow', '😮 Wow'), ('sad', '😢 Sad'), ('angry', '😠 Angry'), ('celebrate', '🎉 Celebrate'), ('support', '💪 Support')], max_length=15, verbose_name='Reaction type')),
                ('object_id', models.PositiveIntegerField(verbose_name='Object ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Content type')),
            ],
            options={
                'verbose_name': 'Reaction',
                'verbose_name_plural': 'Reactions',
                'ordering': ['-created_at'],
            },
        ),
    ]
