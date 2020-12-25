# Generated by Django 2.2.6 on 2019-11-03 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_auto_20191031_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presssensorconfig',
            name='low_alarm',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='presssensorconfig',
            name='low_warning',
            field=models.PositiveSmallIntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='room',
            name='color',
            field=models.IntegerField(choices=[(1, 'Gray'), (2, 'DarkGray'), (3, 'White'), (4, 'Blue'), (5, 'Navy'), (6, 'DarkGreen'), (7, 'Green'), (8, 'Yellow'), (9, 'Orange'), (10, 'Red')], default=3),
        ),
    ]
