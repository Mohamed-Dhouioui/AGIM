# Generated by Django 2.2.6 on 2019-10-31 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0055_auto_20191021_0044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alarm', models.BooleanField(default=True)),
                ('touch', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='configuration',
            name='sound',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Sound'),
        ),
    ]
