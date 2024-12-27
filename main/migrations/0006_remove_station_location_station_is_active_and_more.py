# Generated by Django 4.2 on 2024-05-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_station_latitude_station_longitude'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='location',
        ),
        migrations.AddField(
            model_name='station',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активність'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='station',
            name='current_power',
            field=models.FloatField(verbose_name='Стандартна потужність (МВт)'),
        ),
    ]
