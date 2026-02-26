# Add EducationBoard model for country-based boards (e.g. BD)

from django.db import migrations, models
import django_countries.fields


def load_bd_boards(apps, schema_editor):
    EducationBoard = apps.get_model('institute', 'EducationBoard')
    BD_BOARDS = [
        ('Dhaka Board (BISE, Dhaka)', 'Dhaka'),
        ('Rajshahi Board', 'Rajshahi'),
        ('Cumilla Board', 'Cumilla'),
        ('Jessore Board', 'Jessore'),
        ('Chittagong Board', 'Chittagong'),
        ('Barisal Board', 'Barisal'),
        ('Sylhet Board', 'Sylhet'),
        ('Dinajpur Board', 'Dinajpur'),
        ('Mymensingh Board', 'Mymensingh'),
        ('Bangladesh Madrasah Education Board', 'Madrasah'),
    ]
    for name, code in BD_BOARDS:
        EducationBoard.objects.get_or_create(
            country='BD',
            name=name,
            defaults={'code': code},
        )


def reverse_load_bd_boards(apps, schema_editor):
    EducationBoard = apps.get_model('institute', 'EducationBoard')
    EducationBoard.objects.filter(country='BD').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0014_instituteprofile_institute_type_and_current_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(db_index=True, max_length=2)),
                ('name', models.CharField(max_length=120)),
                ('code', models.CharField(blank=True, help_text='Short code for display', max_length=30)),
            ],
            options={
                'ordering': ['country', 'name'],
            },
        ),
        migrations.AddConstraint(
            model_name='educationboard',
            constraint=models.UniqueConstraint(fields=('country', 'name'), name='institute_educationboard_country_name_uniq'),
        ),
        migrations.RunPython(load_bd_boards, reverse_load_bd_boards),
    ]
