# Generated by Django 2.2.6 on 2020-12-25 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0076_auto_20201225_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comm',
            name='baudrate',
            field=models.CharField(blank=True, default='9600', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='comm',
            name='mac_adress',
            field=models.CharField(blank=True, default='11', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='comm',
            name='object_instance',
            field=models.CharField(blank=True, default='15', max_length=30, null=True),
        ),
    ]
