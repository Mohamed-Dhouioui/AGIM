# Generated by Django 2.2.6 on 2019-10-13 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_remove_flowsensorconfig_metric'),
    ]

    operations = [
        migrations.AddField(
            model_name='presssensorconfig',
            name='delay',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tempsensorconfig',
            name='alarm_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tempsensorconfig',
            name='delay',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
