# Generated by Django 3.0 on 2019-12-17 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0071_auto_20191217_0711'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flowsensorconfig',
            old_name='weight',
            new_name='width',
        ),
    ]
