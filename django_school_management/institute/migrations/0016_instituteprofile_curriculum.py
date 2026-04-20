# Add optional curriculum FK to InstituteProfile

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0015_educationboard'),
        ('curriculum', '0001_initial_curriculum_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteprofile',
            name='curriculum',
            field=models.ForeignKey(
                blank=True,
                help_text='Optional. Curriculum library this institute follows (e.g. Ebtedayi, Dakhil, HSC Science). Used to suggest subjects per class/group.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='institutes',
                to='curriculum.curriculum',
            ),
        ),
    ]
