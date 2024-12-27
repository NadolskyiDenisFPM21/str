import datetime
from django.shortcuts import render, redirect
from django.core.serializers import serialize
from geopy.distance import geodesic
import networkx as nx

from .models import Station


def create_graph():
    """Создаем граф на основе данных из модели Station."""
    graph = nx.Graph()
    stations = Station.objects.all()

    # Добавляем узлы
    for station in stations:
        graph.add_node(
            station.id,
            name=station.name,
            coords=(station.latitude, station.longitude),
            current_power=station.current_power,
            max_power=station.max_power,
            standart_power=station.standart_power,
            block_count=station.block_count,
            is_active=station.is_active,
        )

    # Добавляем ребра с весами (расстояния)
    for station1 in stations:
        for station2 in stations:
            if station1.id != station2.id:
                distance = geodesic(
                    (station1.latitude, station1.longitude),
                    (station2.latitude, station2.longitude),
                ).km
                graph.add_edge(station1.id, station2.id, weight=distance)

    return graph


def redistribute_power(graph, total_required_power, station_id):
    """
    Перераспределяем мощности при включении или выключении станции.
    Если station_id указана, то перераспределяем от неё (для включения или выключения).
    """
    active_nodes = [n for n, attr in graph.nodes(data=True) if attr["is_active"]]
    total_standard_power = sum(
        graph.nodes[node]["standart_power"] * graph.nodes[node]["block_count"]
        for node in active_nodes
    )


    if total_standard_power >= total_required_power:
        # Сброс до стандартной мощности
        for node in active_nodes:
            graph.nodes[node]["current_power"] = graph.nodes[node]["standart_power"]
    else:
        # Добавление мощности
        deficit_power = total_required_power - total_standard_power

        # Проверяем, включена ли станция
        activated_coords = graph.nodes[station_id]["coords"]

        distances = []
        for node in active_nodes:
            if node != station_id:  # Исключаем активированную станцию из перераспределения
                node_coords = graph.nodes[node]["coords"]
                distance = geodesic(activated_coords, node_coords).km
                distances.append((node, distance))

        # Сортировка по расстоянию от активированной станции
        distances.sort(key=lambda x: x[1])

        # Увеличиваем мощности, начиная с ближайших станций
        for node, distance in distances:
            node_attrs = graph.nodes[node]
            available_power = (node_attrs["max_power"] - node_attrs["current_power"]) * node_attrs["block_count"]

            if deficit_power > available_power:
                node_attrs["current_power"] = node_attrs["max_power"]
                deficit_power -= available_power
            else:
                node_attrs["current_power"] += deficit_power / node_attrs["block_count"]
                deficit_power = 0
                break


    # Обновляем данные в базе
    for node in graph.nodes:
        station = Station.objects.get(id=node)
        station.current_power = graph.nodes[node]["current_power"]
        station.save()
        print(f"Станция {station.name}: мощность обновлена до {station.current_power} МВт")



def handle_station_activation(request, target):
    """
    Включение станции с перерасчетом мощностей ближайших станций.
    """
    activated_station = Station.objects.get(id=target)
    activated_station.is_active = True
    activated_station.current_power = activated_station.standart_power
    activated_station.save()

    total_required_power = get_total_required_power()
    graph = create_graph()

    redistribute_power(graph, total_required_power, activated_station.id)

    return redirect("index")


def handle_outage_with_graph(request, target):
    """Обрабатываем отключение станции с использованием графа."""
    outage_station = Station.objects.get(id=target)
    outage_station.current_power = 0
    outage_station.is_active = False
    outage_station.save()

    total_required_power = get_total_required_power()
    graph = create_graph()
    redistribute_power(graph, total_required_power, outage_station.id)

    return redirect("index")


def get_total_required_power():
    """Получаем общую необходимую мощность (пока захардкожено)."""
    return 13000.0  # Пример


def index(request):
    """Главная страница с отображением данных."""
    power_stations = Station.objects.all()
    active_stations = Station.objects.filter(is_active=True)
    total_required_power = get_total_required_power()
    total_current_power = sum(
        s.current_power * s.block_count for s in active_stations
    )
    d_power = total_current_power - total_required_power

    for station in power_stations:
        station.total_power = station.block_count * station.current_power
        power_stations_json = serialize("json", power_stations)

    return render(
        request,
        "index.html",
        {
            "power_stations": power_stations,
            "power_stations_json": power_stations_json,
            "d_power": d_power,
            "total_required_power": total_required_power,
            "total_current_power": total_current_power,
        },
    )
