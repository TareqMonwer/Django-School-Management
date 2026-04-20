# Add gender, applying_for_class, admit_to_semester for BD admission flows

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0032_admissionstudent_optional_academic_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionstudent',
            name='gender',
            field=models.CharField(
                blank=True,
                choices=[('M', 'Male'), ('F', 'Female')],
                help_text='Gender (Male/Female).',
                max_length=1,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='admissionstudent',
            name='applying_for_class',
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text='For school/madrasah: class level (1-10). JSC/JDC fields shown for 9-10.',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='admissionstudent',
            name='admit_to_semester',
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text='Polytechnic: 1 or 4 (when HSC Science eligible for direct 4th sem).',
                null=True,
            ),
        ),
    ]
