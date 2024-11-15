# Структура проекта для ЦОДД

В этом репозитории реализован алгоритм и веб-интерфейс.

# Backend

- **fain.py** - Файл, для изменения названий файлов данных, написанных на кирилеце, чтобы они переводились транслитом.
- **main.py** - Основной код
- **new.py** - Базовый визуализатор
- **test.py** - Первоначальная версия, которая генерирует графы.

## Frontend

### Public
- **public/**
  - **favicon.ico** - Иконка для отображения на вкладке браузера.
  - **index.html** - Основная HTML-страница приложения.

### Src
- **src/** - Исходный код фронтенда.
  - **assets/** - Папка для статических ресурсов, таких как изображения и стили.
    - **img/** - Папка для хранения изображений.
  - **router/** - Маршрутизация приложения Vue.js.
  - **store/** - Vuex хранилище для управления состоянием приложения.
  - **views/** - Основные представления (страницы) приложения.
  - **App.vue** - Главный компонент Vue, содержащий основную разметку.
  - **main.js** - Точка входа для инициализации Vue приложения.

### Конфигурационные файлы
- **babel.config.js** - Конфигурация Babel для трансформации кода JavaScript.
- **jsconfig.json** - Конфигурационный файл для настройки путей и автозавершения в редакторах.
- **package-lock.json** - Файл блокировки зависимостей, фиксирующий версии npm-пакетов.
- **package.json** - Конфигурационный файл npm, содержащий зависимости и скрипты проекта.
- **vue.config.js** - Конфигурационный файл Vue.js.

- **readme.md** - Документация проекта.
