from django.db import models
from django.core.validators import MaxValueValidator


class Station(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    block_count = models.IntegerField(verbose_name="Кількість енергоблоків")
    current_power = models.FloatField(verbose_name="Поточна потужність (МВт)")
    standart_power = models.FloatField(verbose_name="Стандартна потужність (МВт)")
    max_power = models.FloatField(verbose_name="Максимальна потужність (МВт)")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Довгота")
    is_active = models.BooleanField(verbose_name="Активність")
    
    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        verbose_name = 'Електростанція'
        verbose_name_plural = 'Електростанції'
        
        

class Outage(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='outages')
    outage_date = models.DateField(verbose_name="Дата отключения")