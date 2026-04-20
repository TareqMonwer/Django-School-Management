from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0011_instituteprofile_country_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteprofile',
            name='onboarding_completed',
            field=models.BooleanField(default=False),
        ),
    ]
