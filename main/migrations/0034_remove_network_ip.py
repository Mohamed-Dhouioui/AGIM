# Generated by Django 2.2.6 on 2019-10-07 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20191007_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='network',
            name='ip',
        ),
    ]
