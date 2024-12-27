from django.contrib import admin
from .models import Station, Outage
    
    
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'block_count', 'current_power', 'max_power', 'is_active')    
    verbose_name = 'Електростанція'
    verbose_name_plural = 'Електростанції'


@admin.register(Outage)
class OutageAdmin(admin.ModelAdmin):
    list_display = ('id', 'station', 'outage_date')
    verbose_name = 'Відключення'
    verbose_name_plural = 'Відключення'
    