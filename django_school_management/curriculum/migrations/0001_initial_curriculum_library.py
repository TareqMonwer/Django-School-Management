# Curriculum library: Curriculum, CurriculumLevel, Stream, SubjectTemplate, CurriculumSubject

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institute', '0015_educationboard'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=120)),
                ('code', models.CharField(blank=True, help_text='Short code for display (e.g. Ebtedayi, Dakhil, HSC-Science).', max_length=40)),
                ('description', models.TextField(blank=True)),
                ('institute_type', models.CharField(blank=True, choices=[('', 'Any'), ('school', 'School (SSC/HSC)'), ('madrasah', 'Madrasah (Ebtedayi/Dakhil/Alim)'), ('polytechnic', 'Polytechnic')], help_text='Institute type this curriculum is intended for. Blank = any.', max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('display_order', models.PositiveSmallIntegerField(default=0, help_text='Order in lists.')),
                ('board', models.ForeignKey(blank=True, help_text='Education board (e.g. Bangladesh Madrasah Board). Optional.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='curricula', to='institute.educationboard')),
            ],
            options={
                'ordering': ['display_order', 'name'],
                'verbose_name_plural': 'Curricula',
            },
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=60)),
                ('code', models.CharField(help_text='e.g. Science, Arts, Commerce.', max_length=20, unique=True)),
                ('description', models.TextField(blank=True)),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['display_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SubjectTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=120)),
                ('code', models.CharField(help_text='Unique code (e.g. 101, BANGLA, MATH).', max_length=30, unique=True)),
                ('description', models.TextField(blank=True)),
                ('default_theory_marks', models.PositiveIntegerField(default=100)),
                ('default_practical_marks', models.PositiveIntegerField(default=0)),
                ('is_elective', models.BooleanField(default=False, help_text='If True, typically offered as an optional/elective subject.')),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['display_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='CurriculumLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('level_number', models.PositiveSmallIntegerField(help_text='Numeric level (1–12). Used to map to Semester/Class number.')),
                ('name', models.CharField(help_text='Display name (e.g. "Class 1", "Ebtedayi 5", "Dakhil 9").', max_length=80)),
                ('semester_number', models.PositiveSmallIntegerField(blank=True, help_text='Maps to Semester.number (1–12) when curriculum is applied. Defaults to level_number.', null=True)),
                ('streams_applicable', models.BooleanField(default=False, help_text='If True, subjects may be defined per stream (Science/Arts/Commerce) for this level.')),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='curriculum.curriculum')),
            ],
            options={
                'ordering': ['curriculum', 'display_order', 'level_number'],
                'unique_together': {('curriculum', 'level_number')},
            },
        ),
        migrations.CreateModel(
            name='CurriculumSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_compulsory', models.BooleanField(default=True, help_text='If False, subject is elective at this level/stream.')),
                ('display_order', models.PositiveSmallIntegerField(default=0)),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curriculum_subjects', to='curriculum.curriculum')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='curriculum.curriculumlevel')),
                ('stream', models.ForeignKey(blank=True, help_text='Null = common to all streams; set for stream-specific subjects.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='curriculum_subjects', to='curriculum.stream')),
                ('subject_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curriculum_subject_entries', to='curriculum.subjecttemplate')),
            ],
            options={
                'ordering': ['curriculum', 'level', 'stream', 'display_order', 'subject_template'],
                'verbose_name': 'Curriculum subject',
                'verbose_name_plural': 'Curriculum subjects',
                'unique_together': {('curriculum', 'level', 'stream', 'subject_template')},
            },
        ),
    ]
