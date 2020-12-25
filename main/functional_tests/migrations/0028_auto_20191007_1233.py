# Generated by Django 2.2.6 on 2019-10-07 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_configuration_display_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=30)),
                ('ip', models.CharField(default=None, max_length=30)),
                ('password', models.CharField(default=None, max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='configuration',
            name='network',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Network'),
        ),
    ]
