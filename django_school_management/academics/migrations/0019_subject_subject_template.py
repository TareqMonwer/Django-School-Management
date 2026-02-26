# Add optional subject_template FK to Subject (curriculum library link)

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0018_department_institute'),
        ('curriculum', '0001_initial_curriculum_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='subject_template',
            field=models.ForeignKey(
                blank=True,
                help_text='Optional. Link to curriculum library template for this subject.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='subjects',
                to='curriculum.subjecttemplate',
            ),
        ),
    ]
