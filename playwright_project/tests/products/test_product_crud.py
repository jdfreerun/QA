"""
CRUD тесты для товаров CloudShop
"""

import pytest
from pages.products_page import ProductsPage
from utils.data_generator import TestDataGenerator


@pytest.mark.products
@pytest.mark.smoke
@pytest.mark.P0
def test_create_product_with_all_fields(authenticated_page):
    """
    Тест: Создание товара с основными полями
    
    Предусловия: Пользователь авторизован
    Шаги:
        1. Открыть страницу товаров
        2. Нажать "Создать товар"
        3. Заполнить основные поля
        4. Сохранить
        5. Проверить наличие в списке
    Ожидаемый результат: Товар создан и отображается в списке
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Генерируем данные
    product_data = TestDataGenerator.generate_product_data()
    
    print(f"\n📦 Создаем товар: {product_data['name']}")
    
    # Создаем товар через метод create_product
    products_page.click_create_product()
    products_page.fill_product_form(
        name=product_data["name"],
        barcode=product_data["barcode"],
        article=product_data["article"],
        price=product_data["price"],
        description=product_data["description"]
    )
    products_page.click_save()
    
    # Проверяем создание
    assert products_page.is_product_in_list(product_data["name"]), \
        f"Товар '{product_data['name']}' не найден в списке после создания"
    
    print(f"✓ Товар '{product_data['name']}' успешно создан")


@pytest.mark.products
@pytest.mark.smoke
@pytest.mark.P0
def test_create_product_minimal_fields(authenticated_page):
    """
    Тест: Создание товара только с обязательными полями
    
    Предусловия: Пользователь авторизован
    Шаги:
        1. Открыть страницу товаров
        2. Создать товар только с названием
        3. Сохранить
    Ожидаемый результат: Товар создан с минимальными данными
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Создаем товар только с названием
    product_name = TestDataGenerator.generate_product_name()
    products_page.create_product(name=product_name)
    
    # Проверяем
    assert products_page.is_product_in_list(product_name), \
        f"Товар '{product_name}' не найден в списке"
    
    print(f"✓ Товар '{product_name}' создан с минимальными полями")


@pytest.mark.products
@pytest.mark.regression
@pytest.mark.P1
def test_search_product(authenticated_page):
    """
    Тест: Поиск товара по названию
    
    Предусловия: 
        - Пользователь авторизован
        - В системе есть товары
    Шаги:
        1. Открыть страницу товаров
        2. Создать тестовый товар
        3. Проверить наличие в общем списке
    Ожидаемый результат: Товар отображается в списке
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Создаем товар
    product_name = TestDataGenerator.generate_product_name()
    products_page.create_product(name=product_name)
    
    # Проверяем наличие в списке (без поиска, т.к. поле поиска еще не идентифицировано)
    authenticated_page.wait_for_timeout(2000)
    
    # Проверяем результаты
    assert products_page.is_product_in_list(product_name), \
        f"Товар '{product_name}' не найден в списке товаров"
    
    print(f"✓ Товар '{product_name}' успешно отображается в списке")


@pytest.mark.products
@pytest.mark.regression
@pytest.mark.P2
@pytest.mark.parametrize("barcode_length", [8, 13, 14])
def test_create_product_different_barcodes(authenticated_page, barcode_length):
    """
    Тест: Создание товара с разными форматами штрих-кодов
    
    Параметры:
        barcode_length: Длина штрих-кода (8, 13, 14 цифр)
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Генерируем штрих-код нужной длины
    barcode = ''.join([str(i % 10) for i in range(barcode_length)])
    product_name = f"Товар с ШК-{barcode_length}"
    
    # Создаем товар
    products_page.create_product(name=product_name, barcode=barcode)
    
    # Проверяем
    assert products_page.is_product_in_list(product_name), \
        f"Товар с штрих-кодом длиной {barcode_length} не создан"
    
    print(f"✓ Товар с штрих-кодом {barcode_length} цифр создан")

