# Generated by Django 2.2.6 on 2019-10-07 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_auto_20191007_2239'),
    ]

    operations = [
        migrations.RenameField(
            model_name='display',
            old_name='screen_lock',
            new_name='screen_sleep',
        ),
    ]
