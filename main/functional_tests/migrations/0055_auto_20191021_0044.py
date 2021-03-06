# Generated by Django 2.2.6 on 2019-10-21 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_partsensorconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='airflow',
            field=models.PositiveSmallIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='analog',
            field=models.PositiveSmallIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='humidity',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='particles',
            field=models.PositiveSmallIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='pressure',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='temperature',
            field=models.FloatField(default=None, null=True),
        ),
    ]
