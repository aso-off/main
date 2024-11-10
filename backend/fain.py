import os

# Словарь для замены русских букв на латиницу
translit_dict = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
    'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
    'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
    'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ы': 'y', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh',
    'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
    'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts',
    'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ы': 'Y', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'ь':''
}

# Функция для транслитерации
def transliterate(text):
    return ''.join(translit_dict.get(char, char) for char in text)

# Путь к папке с файлами
folder_path = './data'  # Замените на ваш путь

# Получаем список всех файлов в папке
for filename in os.listdir(folder_path):
    # Полный путь к файлу
    old_file = os.path.join(folder_path, filename)
    
    # Проверяем, что это файл, а не папка
    if os.path.isfile(old_file):
        # Создаём новое имя файла
        new_filename = transliterate(filename)
        new_file = os.path.join(folder_path, new_filename)
        
        # Переименовываем файл
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} -> {new_filename}')
