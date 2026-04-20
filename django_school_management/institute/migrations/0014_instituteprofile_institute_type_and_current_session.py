# Generated manually for institute type and current session

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0018_department_institute'),
        ('institute', '0013_alter_city_created_alter_city_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteprofile',
            name='institute_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('school', 'School (e.g. SSC/HSC)'),
                    ('madrasah', 'Madrasah (e.g. Dakhil, Alim, Fazil)'),
                    ('polytechnic', 'Polytechnic Institute'),
                ],
                help_text='Determines terminology (Department vs Group) and admission/counselling flow.',
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='instituteprofile',
            name='current_session',
            field=models.ForeignKey(
                blank=True,
                help_text='Single active academic session for school/madrasah. Leave blank for polytechnic.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='institutes_using_as_current',
                to='academics.academicsession',
            ),
        ),
    ]
