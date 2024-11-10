import random
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import os
import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt

# Задаем область, в которой генерируются объекты
xmin, ymin = 0, 0
xmax, ymax = 1000, 1000

# Количество объектов
num_houses = 50
num_hospitals = 3
num_stops = 5

# Размеры объектов (дома, больницы)
house_size = 20  # размер дома (20x20 м)
hospital_size = 50  # размер больницы (50x50 м)
grid_size = 100  # размер ячейки сетки (100x100 м)

# Создание папки data, если она не существует
output_folder = "data"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Функция для генерации квадратных объектов (дома, больницы)
def generate_square(xmin, ymin, xmax, ymax, size):
    x = random.uniform(xmin, xmax - size)
    y = random.uniform(ymin, ymax - size)
    return Polygon([(x, y), (x + size, y), (x + size, y + size), (x, y + size)])

# Функция для логичного размещения домов вдоль сетки
def generate_logical_layout(xmin, ymin, xmax, ymax, num_houses, house_size, grid_size):
    houses = []
    x_coords = list(range(xmin, xmax, grid_size))
    y_coords = list(range(ymin, ymax, grid_size))
    
    for i in range(num_houses):
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            x = random.choice(x_coords)
            y = random.choice(y_coords)
            if x + house_size <= xmax and y + house_size <= ymax:
                new_house = Polygon([(x, y), (x + house_size, y), (x + house_size, y + house_size), (x, y + house_size)])
                if all(not house.intersects(new_house) for house in houses):
                    houses.append(new_house)
                    placed = True
            attempts += 1
    return houses

# Генерация случайных объектов (дома, больницы)
houses = generate_logical_layout(xmin, ymin, xmax, ymax, num_houses, house_size, grid_size)
hospitals = [generate_square(xmin, ymin, xmax, ymax, hospital_size) for _ in range(num_hospitals)]

# Функция для построения более реалистичных дорог с учетом ландшафта
def generate_realistic_road(start, end, obstacles, existing_roads, max_bend_angle=30):
    line_points = [start]
    num_segments = random.randint(5, 8)
    x1, y1 = start
    x2, y2 = end
    
    for i in range(1, num_segments):
        t = i / num_segments
        bend_factor = random.uniform(-max_bend_angle, max_bend_angle)
        x = x1 * (1 - t) + x2 * t + random.uniform(-bend_factor, bend_factor)
        y = y1 * (1 - t) + y2 * t + random.uniform(-bend_factor, bend_factor)
        
        new_point = Point(x, y)
        new_segment = LineString([line_points[-1], (x, y)])

        # Проверяем, не пересекает ли новый сегмент препятствия
        if not any(obstacle.intersects(new_segment) for obstacle in obstacles) and not any(road.intersects(new_segment) for road in existing_roads):
            line_points.append((x, y))
        else:
            # Если пересекает, корректируем положение сегмента
            adjusted_point = Point(x1 * (1 - t) + x2 * t, y1 * (1 - t) + y2 * t)
            line_points.append(adjusted_point.coords[0])
    
    line_points.append(end)
    return LineString(line_points)

# Генерация дорог между домами и больницами с учетом препятствий
roads = []
obstacles = houses + hospitals  # Препятствия — это дома и больницы
for house in houses:
    closest_hospital = min(hospitals, key=lambda hospital: house.distance(hospital))
    road = generate_realistic_road(house.centroid.coords[0], closest_hospital.centroid.coords[0], obstacles, roads)
    roads.append(road)

# Генерация остановок вдоль дорог (через определенный интервал)
def generate_stops_on_road(road, interval=200):
    stops = []
    road_length = road.length
    num_stops = int(road_length // interval)
    
    for i in range(1, num_stops):
        point_on_road = road.interpolate(i * interval / road_length)
        stops.append(Point(point_on_road.x, point_on_road.y))
        
    return stops

# Размещение остановок вдоль дорог
stops = []
for road in roads:
    stops.extend(generate_stops_on_road(road))

# Создание GeoDataFrame для объектов
houses_gdf = gpd.GeoDataFrame(geometry=houses)
hospitals_gdf = gpd.GeoDataFrame(geometry=hospitals)
stops_gdf = gpd.GeoDataFrame(geometry=stops)
roads_gdf = gpd.GeoDataFrame(geometry=roads)

# Визуализация
fig, ax = plt.subplots(figsize=(10, 10))
houses_gdf.plot(ax=ax, color='blue', label='Дома')
hospitals_gdf.plot(ax=ax, color='red', label='Больницы')
stops_gdf.plot(ax=ax, color='green', marker='s', label='Остановки')
roads_gdf.plot(ax=ax, color='black', linewidth=1, label='Дороги')

plt.legend()
plt.show()

# Сохранение данных в формат shapefile в папку data
try:
    print("Saving houses shapefile...")
    houses_gdf.to_file(os.path.join(output_folder, "houses.shp"))
    print("Houses shapefile saved successfully.")
    
    print("Saving hospitals shapefile...")
    hospitals_gdf.to_file(os.path.join(output_folder, "hospitals.shp"))
    print("Hospitals shapefile saved successfully.")
    
    print("Saving stops shapefile...")
    stops_gdf.to_file(os.path.join(output_folder, "stops.shp"))
    print("Stops shapefile saved successfully.")
    
    print("Saving roads shapefile...")
    roads_gdf.to_file(os.path.join(output_folder, "roads.shp"))
    print("Roads shapefile saved successfully.")
    
except Exception as e:
    print(f"Error while saving shapefiles: {e}")
