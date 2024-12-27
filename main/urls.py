from django.urls import path
from . import views


urlpatterns = [
    path('', view=views.index, name='index'),
    path('deactivate/<int:target>/', view=views.handle_outage_with_graph, name='deactivate'),
    path('activate/<int:target>/', view=views.handle_station_activation, name='activate'),
]
