# Allow optional academic fields for school/madrasah admission (polytechnic still requires them via form)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0031_convert_city_to_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admissionstudent',
            name='exam_name',
            field=models.CharField(
                blank=True,
                choices=[
                    ('HSC', 'Higher Secondary Certificate'),
                    ('SSC', 'Secondary School Certificate'),
                    ('DAKHIL', 'Dakhil Exam'),
                    ('VOCATIONAL', 'Vocational'),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='passing_year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='group',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='board',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='ssc_roll',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='ssc_registration',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='admissionstudent',
            name='gpa',
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=4,
                null=True,
            ),
        ),
    ]
