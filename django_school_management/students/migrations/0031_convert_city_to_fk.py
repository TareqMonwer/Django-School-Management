"""
Convert AdmissionStudent.city from CharField (BD zila codes) to ForeignKey
pointing to institute.City. Handles existing data by:
1. Loading the BD cities fixture so City rows exist.
2. Adding a temporary city_fk column.
3. Mapping old char codes ("01"-"64") to City PKs.
4. Dropping the old city column and renaming city_fk -> city.
"""
import os
from django.db import migrations, models
import django.db.models.deletion


def load_bd_cities_and_map(apps, schema_editor):
    City = apps.get_model('institute', 'City')

    if not City.objects.filter(country='BD').exists():
        from django.core.management import call_command
        fixture_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'institute', 'fixtures', 'bd_cities.json',
        )
        call_command('loaddata', fixture_path, verbosity=0)

    bd_cities = {c.code: c for c in City.objects.filter(country='BD')}

    AdmissionStudent = apps.get_model('students', 'AdmissionStudent')
    for student in AdmissionStudent.objects.all():
        old_code = student.city_legacy
        if old_code and old_code in bd_cities:
            student.city_fk = bd_cities[old_code]
            student.save(update_fields=['city_fk'])


def reverse_map(apps, schema_editor):
    AdmissionStudent = apps.get_model('students', 'AdmissionStudent')
    for student in AdmissionStudent.objects.select_related('city_fk').all():
        if student.city_fk:
            student.city_legacy = student.city_fk.code
            student.save(update_fields=['city_legacy'])


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0030_alter_admissionstudent_admission_policy_agreement_and_more'),
        ('institute', '0011_instituteprofile_country_city'),
    ]

    operations = [
        # 1. Rename old city CharField -> city_legacy
        migrations.RenameField(
            model_name='admissionstudent',
            old_name='city',
            new_name='city_legacy',
        ),
        # 2. Add new FK column as city_fk (nullable)
        migrations.AddField(
            model_name='admissionstudent',
            name='city_fk',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='+',
                to='institute.city',
            ),
        ),
        # 3. Load BD cities fixture and map old codes to FK
        migrations.RunPython(load_bd_cities_and_map, reverse_map),
        # 4. Remove the legacy column
        migrations.RemoveField(
            model_name='admissionstudent',
            name='city_legacy',
        ),
        # 5. Rename city_fk -> city
        migrations.RenameField(
            model_name='admissionstudent',
            old_name='city_fk',
            new_name='city',
        ),
        # 6. Update the field definition to match the model
        migrations.AlterField(
            model_name='admissionstudent',
            name='city',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='students',
                to='institute.city',
            ),
        ),
    ]
