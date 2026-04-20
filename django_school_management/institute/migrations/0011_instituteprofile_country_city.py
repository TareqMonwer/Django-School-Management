from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0010_rename_index_title_instituteprofile_super_admin_index_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteprofile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('code', models.CharField(help_text='Short code or district number (e.g. "13" for Dhaka)', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'cities',
                'ordering': ['name'],
                'unique_together': {('country', 'code')},
            },
        ),
    ]
