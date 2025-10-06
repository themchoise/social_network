
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('career', '0001_initial'),
        ('group', '0001_initial'),
        ('subject', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='admin_groups', to=settings.AUTH_USER_MODEL, verbose_name='Administrators'),
        ),
        migrations.AddField(
            model_name='group',
            name='career',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='career.career', verbose_name='Related career'),
        ),
        migrations.AddField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_groups', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='group',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='subject.subject', verbose_name='Related subject'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.group', verbose_name='Group'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='user_groups', through='group.GroupMembership', to=settings.AUTH_USER_MODEL, verbose_name='Members'),
        ),
        migrations.AlterUniqueTogether(
            name='groupmembership',
            unique_together={('user', 'group')},
        ),
    ]
