from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0011_instituteprofile_country_city'),
        ('teachers', '0005_teacher_employee_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='institute',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='teachers',
                to='institute.instituteprofile',
            ),
        ),
    ]
