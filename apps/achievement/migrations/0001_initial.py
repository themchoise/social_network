
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Achievement name')),
                ('description', models.TextField(verbose_name='Description')),
                ('achievement_type', models.CharField(choices=[('academic', 'Academic'), ('social', 'Social'), ('completion', 'Completion'), ('milestone', 'Milestone'), ('special', 'Special')], max_length=15, verbose_name='Achievement type')),
                ('level', models.CharField(choices=[('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum')], default='bronze', max_length=10, verbose_name='Level')),
                ('points', models.PositiveIntegerField(default=10, verbose_name='Points awarded')),
                ('icon', models.CharField(blank=True, max_length=100, verbose_name='Icon class')),
                ('condition_description', models.TextField(help_text='Description of how to unlock this achievement', verbose_name='Unlock condition')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Achievement',
                'verbose_name_plural': 'Achievements',
                'ordering': ['achievement_type', 'level', 'name'],
            },
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_at', models.DateTimeField(auto_now_add=True, verbose_name='Earned at')),
                ('progress', models.PositiveIntegerField(default=100, help_text='Progress percentage (0-100)', verbose_name='Progress')),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_achievements', to='achievement.achievement', verbose_name='Achievement')),
            ],
            options={
                'verbose_name': 'User Achievement',
                'verbose_name_plural': 'User Achievements',
                'ordering': ['-earned_at'],
            },
        ),
    ]
