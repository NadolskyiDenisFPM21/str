# Generated by Django 4.2 on 2024-05-23 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_station_standart_power_alter_station_current_power'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outage_date', models.DateField(verbose_name='Дата отключения')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outages', to='main.station')),
            ],
        ),
        migrations.DeleteModel(
            name='TPS',
        ),
    ]
