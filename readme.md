# README: Система сборки Python приложений

## Описание

Этот проект содержит два скрипта для сборки Python-приложений в исполняемые файлы:

1. **`build.py`** - Полная сборка основного приложения и тестовой системы
2. **`rebuild.py`** - Быстрое обновление EXE-файла без пересборки зависимостей

## Требования

- Python >=3.10 <3.12
- PyInstaller 4.0+
- FFmpeg (если используется в проекте)

## Установка

1. Установите зависимости:
```bash
pip install pyinstaller
```

2. Для работы с FFmpeg:

```bash
Windows (скачать и распаковать в папку проекта /asstes/)
``` 

3. `Pretrained/`должна находтся в `assests/`

3. Файлы `build.py` и `rebuild.py` должны находится в корневой папке проекта

## Использование

### Полная сборка (build.py)

Собирает оба приложения (основное и тестовое) в папку `dist/start_app`:

```bash
python build.py
```

**Особенности:**
- Собирает основное приложение из `start_app.py`
- Собирает тестовую систему из `test_system.py`
- Переносит ресурсы (`assets/`, `static/`, `ffmpeg/`)
- Полностью очищает предыдущие сборки

### Быстрое обновление (rebuild.py)

Обновляет только EXE-файл для указанного скрипта:

```bash
python rebuild.py start_app.py
# Или для тестовой системы
python rebuild.py test_system.py
```

**Особенности:**
- Работает  быстрее полной сборки
- Не пересобирает зависимости
- Создает backup старого EXE
- Подходит только когда:
  - Не менялись импорты
  - Не обновлялись зависимости
  - Не изменялись ресурсы

## Структура проекта

```
project/
├── build.py          # Скрипт полной сборки
├── rebuild.py        # Скрипт быстрого обновления
├── start_app.py      # Основное приложение
├── test_system.py    # Тестовая система
├── assets/           # Ресурсы приложения
├── static/           # Статические файлы
├── ffmpeg/           # Библиотеки FFmpeg
├── templates/        # Шаблоны
├── settings.yaml     # Конфигурация
├──.venv/             # Виртуальное окружение
├──src/               # Подсистемы
├──tests/             # test files app
└── .env              # Переменные окружения
```

## Особенности реализации

1. **Безопасность**:
   - Проверка существования всех необходимых файлов
   - Резервное копирование перед заменой
   - Подробное логирование ошибок

2. **Оптимизация**:
   - Минимальный уровень логов PyInstaller (ERROR)
   - Исключение неиспользуемых модулей
   - Быстрая очистка временных файлов

3. **Поддержка FFmpeg**:
   - Автоматическое включение в сборку
   - Проверка доступности

## Советы по использованию

1. Для первого запуска всегда используйте `build.py`
2. Для обновления кода без изменения зависимостей используйте `rebuild.py`
3. При изменении `import` или ресурсов требуется полная пересборка
4. Проверяйте вывод скриптов для выявления проблем
5. Использовать `build.py` и `rebuild.py` из окружния, применяемого в приложении

## Логирование

Оба скрипта выводят подробную информацию о процессе:
- ✅ Успешные операции
- ❌ Ошибки с описанием
- ⚠️ Предупреждения
- 🔄 Действия с файлами

