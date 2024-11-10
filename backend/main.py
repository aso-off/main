import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
import math
import heapq
import numpy as np
import matplotlib.pyplot as plt
from heapq import heappush, heappop
import sys
sys.path.append(r"c:\users\work\desktop\newhack\myenv\lib\site-packages")
from rtree import index
from collections import deque


path = './data/House_1ochered_ZhK.shp'
path1 = './data/Ostanovki_OT.shp'
path2 = './data/Streets_ishodnye.shp'
path3 = './data/Doma_ishodnye.shp'

# Загрузка shapefile с использованием GeoPandas
ddd = gpd.read_file(path)  # Полигоны
ppp = gpd.read_file(path1)  # Остановки
streets = gpd.read_file(path2)  # Улицы 
Doma = gpd.read_file(path3) # Дома
# Извлекаем координаты для каждого объекта геометрии из полигонов
polygons_coords = []
for geom in ddd.geometry:
    if isinstance(geom, Polygon):
        polygons_coords.append(list(geom.exterior.coords))
    elif isinstance(geom, MultiPolygon):
        for polygon in geom.geoms:
            polygons_coords.append(list(polygon.exterior.coords))

# Создаем полигоны из координат
polygons = [Polygon(coords) for coords in polygons_coords]

Doma_coords = []
for geom in Doma.geometry:
    if isinstance(geom, Polygon):
        Doma_coords.append(list(geom.exterior.coords))
    elif isinstance(geom, MultiPolygon):
        for polygon in geom.geoms:
            Doma_coords.append(list(polygon.exterior.coords))

Domas = [Polygon(coords) for coords in Doma_coords]

# Преобразуем данные для остановок в точки
stop = []
for _, row in ppp.iterrows():
    coords = row.geometry.coords
    if coords:
        point = Point(coords[0])
        stop.append(point)

# Индексируем препятствия для быстрого поиска
obstacle_index = index.Index()
for idx, polygon in enumerate(polygons):
    obstacle_index.insert(idx, polygon.bounds)
for idx, polygon in enumerate(Domas):
    obstacle_index.insert(idx, polygon.bounds)

# Функция эвристики (евклидово расстояние)
def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# Функция для поиска соседей
def get_neighbors(node):
    x, y = node
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return neighbors

# Функция для проверки, является ли клетка допустимой
def is_valid_move(node, obstacle_index):
    point = Point(node)
    possible_matches = list(obstacle_index.intersection((point.x, point.y, point.x, point.y)))
    
    for idx in possible_matches:
        # Проверка на допустимость индекса в пределах списка `polygons` и `Domas`
        if idx < len(polygons) and polygons[idx].contains(point):
            return False
        elif idx < len(Domas) and Domas[idx].contains(point):
            return False
    return True


# Алгоритм A* для генерации пути
# BFS для генерации пути
def generate_road(start, end, obstacles):
    queue = deque([start])
    came_from = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            if neighbor not in came_from and is_valid_move(neighbor, obstacle_index):
                queue.append(neighbor)
                came_from[neighbor] = current

    print("Путь не найден.")
    return None

# Генерация дорог от домов к ближайшим остановкам
def generate_realistic_road(start, end, obstacles):
    road = generate_road(start, end, obstacles)
    if road:
        return road
    else:
        print("Путь не найден.")
        return None

# Генерация дорог от домов к ближайшим остановкам
roads = []
obstacles = polygons + stop  # Препятствия — это дома и остановки

# Перебираем все дома
for house in polygons:
    closest_stop = None
    min_distance = float('inf')
    
    for sto in stop:
        if sto is not None:
            distance = house.distance(sto)
            if distance < min_distance:
                min_distance = distance
                closest_stop = sto
    
    if closest_stop is not None:
        house_coords = house.exterior.coords[0]
        stop_coords = closest_stop.coords[0]
        
        road = generate_realistic_road(house_coords, stop_coords, obstacles)
        
        if road:
            roads.append(road)

# Создаем GeoDataFrame для дорог
roads_gdf = gpd.GeoDataFrame(geometry=roads)
# Создаем GeoDataFrame для полигонов
polygons_gdf = gpd.GeoDataFrame(geometry=polygons)
# Создаем GeoDataFrame для точек остановок
stops_gdf = gpd.GeoDataFrame(geometry=stop)
# Создаем GeoDataFrame для улиц
streets_gdf = gpd.GeoDataFrame(geometry=streets.geometry)

# Устанавливаем CRS для всех объектов, например, WGS84
crs = "EPSG:4326"
polygons_gdf.set_crs(crs, allow_override=True, inplace=True)
stops_gdf.set_crs(crs, allow_override=True, inplace=True)
roads_gdf.set_crs(crs, allow_override=True, inplace=True)
streets_gdf.set_crs(crs, allow_override=True, inplace=True)

# Визуализация
fig, ax = plt.subplots(figsize=(10, 10))
polygons_gdf.plot(ax=ax, color='lightblue', edgecolor='black', label='Дома')
roads_gdf.plot(ax=ax, color='orange', linewidth=2, label='Дороги')
stops_gdf.plot(ax=ax, color='green', edgecolor='black', label='Остановки')
streets_gdf.plot(ax=ax, color='grey', linewidth=1, linestyle='--', label='Улицы')

plt.title("Дома, улицы и дороги к ближайшим остановкам", fontsize=16)

# Добавляем легенду
ax.legend()

# Отображаем график
plt.show()
