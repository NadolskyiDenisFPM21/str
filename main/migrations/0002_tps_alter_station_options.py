# Generated by Django 4.2 on 2024-04-14 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TPS',
            fields=[
                ('station_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.station')),
            ],
            options={
                'verbose_name': 'Теплоелектростанція',
                'verbose_name_plural': 'Теплоелектростанції',
            },
            bases=('main.station',),
        ),
        migrations.AlterModelOptions(
            name='station',
            options={'verbose_name': 'Електростанція', 'verbose_name_plural': 'Електростанції'},
        ),
    ]
