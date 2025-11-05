# Playwright Python Project

Проект для автоматизации тестирования на Playwright с использованием Python и pytest.

## Структура проекта

```
playwright_project/
├── tests/
│   └── test_cloudshop.py    # Тесты
├── requirements.txt          # Зависимости проекта
├── pytest.ini               # Конфигурация pytest
└── README.md                # Документация
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

Запуск всех тестов:
```bash
pytest
```

Запуск конкретного теста:
```bash
pytest tests/test_cloudshop.py
```

Запуск с подробным выводом:
```bash
pytest -v
```

Запуск с HTML отчетом:
```bash
pytest --html=report.html --self-contained-html
```

## Тесты

### test_open_cloudshop_page
Проверяет открытие главной страницы cloudshop.ru и проверяет основные элементы.

### test_login_and_create_product
Полный E2E тест для работы с товарами в CloudShop:
1. Авторизация на web.cloudshop.ru
2. Переход в раздел "Товары и услуги"
3. Создание нового товара с заполнением всех полей
4. Сохранение товара
5. Проверка успешного создания

**Требования:**
- Создайте файл `.env` в корне проекта с учетными данными:
```
CLOUDSHOP_EMAIL=your_email@example.com
CLOUDSHOP_PASSWORD=your_password
```

## Примечания

- Убедитесь, что у вас установлен Python 3.8 или выше
- Playwright поддерживает Chromium, Firefox и WebKit браузеры
- По умолчанию тесты запускаются в headless режиме

