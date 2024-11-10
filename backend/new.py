import geopandas as gpd
import matplotlib.pyplot as plt

# Путь к файлу .shp
file_path = ".shp"  # Замените на ваш путь к файлу

# Загрузка данных
data = gpd.read_file(file_path)

# Визуализация данных
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
data.plot(ax=ax, color='skyblue', edgecolor='black')

# Настройка отображения
ax.set_title("Геопространственные данные из Shapefile")
ax.set_xlabel("Долгота")
ax.set_ylabel("Широта")
plt.show()
