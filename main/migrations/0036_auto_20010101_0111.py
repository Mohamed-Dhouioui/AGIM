# Generated by Django 2.2.6 on 2001-01-01 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20191007_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Display',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sceen_lock', models.BooleanField(default=False)),
                ('off_time', models.PositiveSmallIntegerField(default=60)),
                ('lock_time', models.PositiveSmallIntegerField(default=30)),
            ],
        ),
        migrations.AddField(
            model_name='configuration',
            name='display',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Display'),
        ),
    ]