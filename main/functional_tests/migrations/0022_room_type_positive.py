# Generated by Django 2.2.6 on 2019-10-04 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20191004_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='type_positive',
            field=models.BooleanField(default=True),
        ),
    ]
