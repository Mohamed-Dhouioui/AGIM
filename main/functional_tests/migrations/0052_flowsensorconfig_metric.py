# Generated by Django 2.2.6 on 2019-10-13 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_auto_20191013_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowsensorconfig',
            name='metric',
            field=models.BooleanField(default=True),
        ),
    ]