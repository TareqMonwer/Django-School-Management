# Generated by Django 2.2.13 on 2021-02-04 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0006_instituteprofile_motto'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteprofile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='instituteprofile',
            name='motto',
            field=models.TextField(blank=True, null=True),
        ),
    ]
