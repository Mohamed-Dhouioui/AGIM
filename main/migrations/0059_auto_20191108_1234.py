# Generated by Django 2.2.6 on 2019-11-08 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0058_auto_20191103_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='presssensorconfig',
            name='in_h2o',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tempsensorconfig',
            name='celsius',
            field=models.BooleanField(default=True),
        ),
    ]
