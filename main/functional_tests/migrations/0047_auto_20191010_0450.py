# Generated by Django 2.2.6 on 2019-10-10 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_auto_20191010_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
