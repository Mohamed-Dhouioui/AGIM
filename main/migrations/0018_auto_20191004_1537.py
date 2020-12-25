# Generated by Django 2.2.6 on 2019-10-04 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_presssensorconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humsensorconfig',
            name='high_alarm',
            field=models.FloatField(default=55.0),
        ),
        migrations.AlterField(
            model_name='humsensorconfig',
            name='high_warning',
            field=models.FloatField(default=60.0),
        ),
        migrations.AlterField(
            model_name='humsensorconfig',
            name='low_alarm',
            field=models.FloatField(default=40.0),
        ),
        migrations.AlterField(
            model_name='humsensorconfig',
            name='low_warning',
            field=models.FloatField(default=45.0),
        ),
    ]