
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0001_initial'),
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['semester', 'name'], 'verbose_name': 'Subject', 'verbose_name_plural': 'Subjects'},
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='subject',
            name='career',
        ),
        migrations.AddField(
            model_name='subject',
            name='career',
            field=models.ManyToManyField(related_name='subjects', to='career.career', verbose_name='Careers'),
        ),
    ]
