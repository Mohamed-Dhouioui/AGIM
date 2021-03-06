# Generated by Django 2.2.6 on 2019-10-04 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_delete_measurement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(default=None)),
                ('humidity', models.FloatField(default=None)),
                ('pressure', models.FloatField(default=None)),
                ('airflow', models.PositiveSmallIntegerField(default=None)),
                ('analog', models.PositiveSmallIntegerField(default=None)),
                ('particles', models.PositiveSmallIntegerField(default=None)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Room')),
            ],
        ),
    ]
