# Generated by Django 2.2.6 on 2019-10-08 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_auto_20191007_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='do_lock',
            field=models.BooleanField(default=False),
        ),
    ]