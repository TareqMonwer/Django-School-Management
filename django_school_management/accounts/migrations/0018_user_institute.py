from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_user_approval_status'),
        ('institute', '0011_instituteprofile_country_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='institute',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='users',
                to='institute.instituteprofile',
            ),
        ),
    ]
