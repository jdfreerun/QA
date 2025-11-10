# Playwright Python Project — CloudShop Automation

Проект для автоматизации тестирования CloudShop на Playwright с использованием Python и pytest.

## Структура проекта

```
playwright_project/
├── pages/                    # Page Object Model
│   ├── base_page.py         # Базовый класс
│   ├── login_page.py        # Страница авторизации
│   └── products_page.py     # Страница товаров
├── utils/                    # Утилиты
│   └── data_generator.py    # Генератор тестовых данных
├── tests/                    # Тесты
│   ├── auth/                # Тесты авторизации
│   │   └── test_login.py
│   └── products/            # Тесты товаров
│       ├── test_product_crud.py
│       └── test_product_extended.py
├── config/                   # Конфигурация
├── data/                     # Тестовые данные
├── conftest.py              # Глобальные fixtures
├── pytest.ini               # Конфигурация pytest
├── requirements.txt          # Зависимости
├── .env                      # Учетные данные (не в git)
└── .gitignore               # Игнорируемые файлы
```

## Установка

1. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # На macOS/Linux
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Установите браузеры Playwright:
```bash
playwright install
```

## Запуск тестов

```bash
# Все тесты
pytest -v

# Только smoke тесты (критические)
pytest -m smoke -v

# Только тесты товаров
pytest -m products -v

# Только тесты авторизации
pytest -m auth -v

# Критические тесты (P0)
pytest -m P0 -v

# Конкретный модуль
pytest tests/products/ -v

# С подробным выводом
pytest -v -s

# Параллельный запуск (требует pytest-xdist)
pip install pytest-xdist
pytest -n 4 -v
```

## Реализованные тесты

### Модуль: Авторизация (4 теста)
- **test_login_success** — успешная авторизация
- **test_login_invalid_password** — неверный пароль
- **test_login_empty_fields** — валидация пустых полей
- **test_logout** — выход из системы

### Модуль: Товары — базовые операции (6 тестов)
- **test_create_product_with_all_fields** — создание с основными полями
- **test_create_product_minimal_fields** — создание с минимумом полей
- **test_search_product** — проверка отображения в списке
- **test_create_product_different_barcodes[8/13/14]** — вариации штрих-кодов

### Модуль: Товары — расширенные поля (4 теста)
- **test_create_product_with_extended_fields** — все поля (dropdown, цены, габариты)
- **test_create_product_with_dimensions** — габариты и вес
- **test_create_product_with_pricing** — ценообразование
- **test_create_product_with_min_stock** — минимальный остаток

**Всего**: 14 автотестов

## Покрытие полей товара

### ✅ Полностью реализовано:
- Наименование, штрих-код, артикул
- Единица измерения (searchable dropdown)
- Описание
- Страна (searchable dropdown)
- Цены: закупка, наценка, продажа
- Габариты: высота, ширина, глубина
- Вес
- Минимальный остаток
- Код налога (searchable dropdown)

## Настройка

### Требования
- Python 3.8+
- Создайте файл `.env` в корне проекта:
```env
CLOUDSHOP_EMAIL=your_email@example.com
CLOUDSHOP_PASSWORD=your_password
```

## Примечания

- Убедитесь, что у вас установлен Python 3.8 или выше
- Playwright поддерживает Chromium, Firefox и WebKit браузеры
- По умолчанию тесты запускаются в headless режиме

