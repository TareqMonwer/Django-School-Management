from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0011_instituteprofile_country_city'),
        ('academics', '0017_alter_subject_practical_marks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='institute',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='departments',
                to='institute.instituteprofile',
            ),
        ),
    ]
