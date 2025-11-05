# Архитектура автотестов CloudShop

## Принципы проектирования

### 1. Page Object Model (POM)
Каждая страница/компонент представлена отдельным классом с инкапсулированными локаторами и методами.

### 2. Fixtures и переиспользование кода
Общая логика (авторизация, создание тестовых данных) вынесена в fixtures.

### 3. Изоляция тестов
Каждый тест независим и может выполняться в любом порядке.

### 4. Data-Driven Testing
Параметризация тестов для проверки разных сценариев с разными данными.

---

## Структура Page Objects

### Базовый класс

```python
# pages/base_page.py
class BasePage:
    def __init__(self, page):
        self.page = page
        
    def navigate(self, url):
        self.page.goto(url)
        
    def click(self, locator):
        self.page.click(locator)
        
    def fill(self, locator, value):
        self.page.fill(locator, value)
        
    def wait_for_load(self, timeout=5000):
        self.page.wait_for_timeout(timeout)
```

### Страница авторизации

```python
# pages/login_page.py
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Локаторы
    EMAIL_INPUT = 'input[placeholder*="Email"]'
    PASSWORD_INPUT = 'input[placeholder*="Пароль"]'
    LOGIN_BUTTON = 'button:has-text("войти")'
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://web.cloudshop.ru/anonymous/login/"
    
    def open(self):
        self.navigate(self.url)
        
    def login(self, email, password):
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_load(3000)
```

### Страница товаров

```python
# pages/products_page.py
from pages.base_page import BasePage

class ProductsPage(BasePage):
    # Локаторы
    CREATE_BUTTON = 'a:has-text("Создать товар")'
    SEARCH_INPUT = 'input[type="search"]'
    MODAL_NAME_INPUT = '[ui-view="modal"] input[type="text"]'
    MODAL_BARCODE_INPUT = 'input[placeholder="Введите штрих-код"]'
    MODAL_ARTICLE_INPUT = 'input[placeholder="Введите артикул"]'
    SAVE_BUTTON = '.cs.sidebar a.ui.button.green:has-text("Сохранить")'
    
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://web.cloudshop.ru/card/catalog/list"
    
    def open(self):
        self.navigate(self.url)
        
    def create_product(self, name, barcode=None, article=None):
        self.click(self.CREATE_BUTTON)
        self.wait_for_load(2000)
        
        # Заполняем поля
        modal_inputs = self.page.locator(self.MODAL_NAME_INPUT)
        if modal_inputs.count() > 1:
            modal_inputs.nth(1).fill(name)
            
        if barcode:
            self.fill(self.MODAL_BARCODE_INPUT, barcode)
        if article:
            self.fill(self.MODAL_ARTICLE_INPUT, article)
            
        self.click(self.SAVE_BUTTON)
        self.wait_for_load(3000)
    
    def search_product(self, product_name):
        self.fill(self.SEARCH_INPUT, product_name)
        self.wait_for_load(1000)
        
    def is_product_in_list(self, product_name):
        return self.page.evaluate(f"""
            (name) => {{
                const cells = Array.from(document.querySelectorAll('td, div'));
                return cells.some(cell => cell.innerText.includes(name));
            }}
        """, product_name)
```

---

## Fixtures

### conftest.py

```python
import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from pages.login_page import LoginPage

load_dotenv()

@pytest.fixture(scope="session")
def browser_context():
    """Создает браузер для всей сессии"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-gpu", "--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)
        yield context
        context.close()
        browser.close()

@pytest.fixture(scope="function")
def page(browser_context):
    """Создает новую страницу для каждого теста"""
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def authenticated_page(page):
    """Фикстура для авторизованной сессии"""
    login_page = LoginPage(page)
    login_page.open()
    
    email = os.getenv("CLOUDSHOP_EMAIL")
    password = os.getenv("CLOUDSHOP_PASSWORD")
    
    login_page.login(email, password)
    yield page

@pytest.fixture(scope="function")
def test_product_data():
    """Генерирует данные для тестового товара"""
    import random
    return {
        "name": f"Тестовый товар {random.randint(1000, 9999)}",
        "barcode": f"{random.randint(1000000000000, 9999999999999)}",
        "article": f"ART-{random.randint(100, 999)}",
        "price": random.randint(100, 10000)
    }
```

---

## Пример использования

```python
# tests/products/test_product_crud.py
import pytest
from pages.products_page import ProductsPage

def test_create_product_positive(authenticated_page, test_product_data):
    """
    Тест: Создание товара с валидными данными
    
    Предусловия: Пользователь авторизован
    Шаги:
        1. Открыть страницу товаров
        2. Создать товар с валидными данными
        3. Проверить появление товара в списке
    Ожидаемый результат: Товар успешно создан и отображается в списке
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Создаем товар
    products_page.create_product(
        name=test_product_data["name"],
        barcode=test_product_data["barcode"],
        article=test_product_data["article"]
    )
    
    # Проверяем
    assert products_page.is_product_in_list(test_product_data["name"]), \
        f"Товар {test_product_data['name']} не найден в списке"

@pytest.mark.parametrize("field_name,invalid_value", [
    ("name", ""),  # Пустое название
    ("name", "A" * 1000),  # Слишком длинное название
    ("price", "-100"),  # Отрицательная цена
])
def test_create_product_validation(authenticated_page, field_name, invalid_value):
    """
    Тест: Валидация полей при создании товара
    
    Проверяет, что система корректно обрабатывает невалидные данные
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Попытка создать товар с невалидными данными
    # Ожидается ошибка валидации
    # ... логика теста
```

---

## Утилиты

### Генератор тестовых данных

```python
# utils/data_generator.py
import random
from faker import Faker

fake = Faker('ru_RU')

class TestDataGenerator:
    @staticmethod
    def generate_product():
        return {
            "name": fake.word().capitalize() + " " + fake.word(),
            "barcode": str(random.randint(1000000000000, 9999999999999)),
            "article": f"ART-{random.randint(100, 999)}",
            "price": random.randint(100, 10000),
            "description": fake.text(max_nb_chars=200)
        }
    
    @staticmethod
    def generate_client():
        return {
            "name": fake.name(),
            "phone": fake.phone_number(),
            "email": fake.email()
        }
    
    @staticmethod
    def generate_supplier():
        return {
            "name": fake.company(),
            "inn": str(random.randint(1000000000, 9999999999)),
            "phone": fake.phone_number()
        }
```

### API клиент

```python
# utils/api_client.py
import requests
import os

class CloudShopAPI:
    def __init__(self):
        self.base_url = "https://web.cloudshop.ru/api"
        self.token = None
    
    def authenticate(self, email, password):
        response = requests.post(f"{self.base_url}/auth", json={
            "email": email,
            "password": password
        })
        self.token = response.json()["token"]
        return self.token
    
    def get_products(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.base_url}/products", headers=headers)
        return response.json()
    
    def create_product(self, product_data):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(
            f"{self.base_url}/products", 
            headers=headers,
            json=product_data
        )
        return response.json()
```

---

## Конфигурация окружений

```python
# config/environments.py
class Config:
    PROD = {
        "base_url": "https://web.cloudshop.ru",
        "api_url": "https://web.cloudshop.ru/api"
    }
    
    STAGE = {
        "base_url": "https://stage.cloudshop.ru",
        "api_url": "https://stage.cloudshop.ru/api"
    }
    
    DEV = {
        "base_url": "https://dev.cloudshop.ru",
        "api_url": "https://dev.cloudshop.ru/api"
    }
    
    @staticmethod
    def get_env(env_name="PROD"):
        return getattr(Config, env_name.upper())
```

---

## Маркеры pytest

```ini
# pytest.ini
[pytest]
markers =
    smoke: Smoke tests (critical functionality)
    regression: Regression tests
    P0: Priority 0 - Critical
    P1: Priority 1 - High
    P2: Priority 2 - Medium
    P3: Priority 3 - Low
    slow: Slow running tests
    ui: UI tests
    api: API tests
    auth: Authentication tests
    products: Product tests
    documents: Document tests
    reports: Report tests
```

---

## Запуск тестов

```bash
# Smoke тесты
pytest -m smoke

# Критические тесты
pytest -m "P0 or P1"

# Только товары
pytest -m products

# Параллельный запуск
pytest -n 4

# С отчетом Allure
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Метрики и KPI

### Качественные метрики
- Test Coverage — покрытие функционала
- Test Pass Rate — процент прохождения тестов
- Defect Detection — процент найденных багов
- Test Execution Time — время выполнения тестов

### Целевые показатели
- Pass Rate: >95%
- Execution Time (полный набор): <30 минут
- Execution Time (smoke): <5 минут
- Flaky Tests: <2%

### Отчетность
- Ежедневные smoke тесты в Slack/Email
- Еженедельные regression отчеты
- Ежемесячные метрики покрытия

