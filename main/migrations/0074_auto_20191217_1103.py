# Generated by Django 3.0 on 2019-12-17 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0073_auto_20191217_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowsensorconfig',
            name='diameter',
            field=models.FloatField(default=203.0),
        ),
    ]
