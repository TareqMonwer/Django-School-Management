# Generated by Django 2.2.13 on 2021-02-08 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210129_0242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='account_approved',
        ),
    ]
