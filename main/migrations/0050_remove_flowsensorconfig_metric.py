# Generated by Django 2.2.6 on 2019-10-13 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_auto_20191013_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flowsensorconfig',
            name='metric',
        ),
    ]
