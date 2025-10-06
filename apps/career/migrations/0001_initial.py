
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Full name of the career', max_length=200, verbose_name='Career name')),
                ('code', models.CharField(help_text='Unique career code (e.g.: ENG001, MED002)', max_length=20, unique=True, verbose_name='Code')),
                ('acronym', models.CharField(blank=True, help_text='Career acronym (e.g.: CSE, MED, ENG)', max_length=10, verbose_name='Acronym')),
                ('description', models.TextField(help_text='Detailed career description', verbose_name='Description')),
                ('career_type', models.CharField(choices=[('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('technical', 'Technical'), ('specialization', 'Specialization'), ('master', 'Master'), ('doctorate', 'Doctorate')], default='undergraduate', max_length=20, verbose_name='Career type')),
                ('duration_semesters', models.PositiveIntegerField(help_text='Total number of semesters for the career', verbose_name='Duration in semesters')),
                ('duration_years', models.PositiveIntegerField(help_text='Total number of years for the career', verbose_name='Duration in years')),
                ('total_credits', models.PositiveIntegerField(help_text='Total academic credits required', verbose_name='Total credits')),
                ('modality', models.CharField(choices=[('presential', 'Presential'), ('virtual', 'Virtual'), ('hybrid', 'Hybrid'), ('distance', 'Distance')], default='presential', max_length=15, verbose_name='Modality')),
                ('faculty', models.CharField(help_text='Faculty to which the career belongs', max_length=100, verbose_name='Faculty')),
                ('department', models.CharField(blank=True, help_text='Specific department within the faculty', max_length=100, verbose_name='Department')),
                ('is_active', models.BooleanField(default=True, help_text='Whether the career is available for enrollment', verbose_name='Active career')),
                ('requires_admission_exam', models.BooleanField(default=False, verbose_name='Requires admission exam')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('max_students_per_semester', models.PositiveIntegerField(blank=True, help_text='Maximum number of students that can enroll per semester', null=True, verbose_name='Max students per semester')),
            ],
            options={
                'verbose_name': 'Career',
                'verbose_name_plural': 'Careers',
                'ordering': ['name'],
            },
        ),
    ]
