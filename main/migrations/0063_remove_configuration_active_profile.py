# Generated by Django 3.0 on 2019-12-06 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0062_auto_20191206_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='active_profile',
        ),
    ]
