# Generated by Django 3.0 on 2019-12-17 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0072_auto_20191217_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowsensorconfig',
            name='average',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='flowsensorconfig',
            name='k_factor',
            field=models.PositiveSmallIntegerField(default=100),
        ),
    ]