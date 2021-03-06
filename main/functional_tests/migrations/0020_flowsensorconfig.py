# Generated by Django 2.2.6 on 2019-10-04 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20191004_1542'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowSensorConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alarm_active', models.BooleanField(default=False)),
                ('profile', models.PositiveSmallIntegerField(default=1)),
                ('low_alarm', models.PositiveSmallIntegerField(default=12)),
                ('low_warning', models.PositiveSmallIntegerField(default=14)),
                ('high_alarm', models.PositiveSmallIntegerField(default=25)),
                ('high_warning', models.PositiveSmallIntegerField(default=20)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Room')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
