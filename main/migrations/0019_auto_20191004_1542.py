# Generated by Django 2.2.6 on 2019-10-04 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20191004_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempsensorconfig',
            name='high_alarm',
            field=models.FloatField(default=29.0),
        ),
        migrations.AlterField(
            model_name='tempsensorconfig',
            name='high_warning',
            field=models.FloatField(default=26.0),
        ),
        migrations.AlterField(
            model_name='tempsensorconfig',
            name='low_alarm',
            field=models.FloatField(default=19.0),
        ),
        migrations.AlterField(
            model_name='tempsensorconfig',
            name='low_warning',
            field=models.FloatField(default=22.0),
        ),
    ]
