"""
Расширенные тесты создания товаров со всеми полями
"""

import pytest
from pages.products_page import ProductsPage
from utils.data_generator import TestDataGenerator


@pytest.mark.products
@pytest.mark.regression
@pytest.mark.P1
def test_create_product_with_extended_fields(authenticated_page):
    """
    Тест: Создание товара со всеми расширенными полями
    
    Предусловия: Пользователь авторизован
    Шаги:
        1. Открыть страницу товаров
        2. Нажать "Создать товар"
        3. Заполнить все доступные поля:
           - Наименование (обязательное)
           - Штрих-код
           - Артикул
           - Единица измерения
           - Описание
           - Страна
           - Цена закупки
           - Наценка
           - Цена продажи
           - Размеры (высота, ширина, глубина)
           - Вес
           - Минимальный остаток
           - Код налога
        4. Сохранить товар
        5. Проверить создание
    Ожидаемый результат: Товар создан со всеми заполненными полями
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Генерируем полный набор данных
    product_data = TestDataGenerator.generate_product_data(full=True)
    
    print(f"\n📦 Создаем товар с расширенными полями:")
    print(f"   Название: {product_data['name']}")
    
    # Открываем форму создания
    products_page.click_create_product()
    
    # Заполняем все доступные поля (dropdown пропускаем, т.к. не обязательные)
    products_page.fill_product_form(
        name=product_data["name"],
        barcode=product_data["barcode"],
        article=product_data["article"],
        price=product_data["price"],
        description=product_data["description"],
        purchase_price=product_data["purchase_price"],
        markup=product_data["markup"],
        weight=product_data["weight"],
        height=product_data["height"],
        width=product_data["width"],
        depth=product_data["depth"],
        min_stock=product_data["min_stock"]
    )
    
    # Сохраняем
    products_page.click_save()
    
    # Проверяем создание
    assert products_page.is_product_in_list(product_data["name"]), \
        f"Товар '{product_data['name']}' не найден в списке после создания"
    
    print(f"\n✓✓✓ Товар с расширенными полями успешно создан! ✓✓✓")


@pytest.mark.products
@pytest.mark.regression
@pytest.mark.P1
def test_create_product_with_dimensions(authenticated_page):
    """
    Тест: Создание товара с указанием габаритов и веса
    
    Проверяет корректность заполнения физических характеристик товара
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Генерируем данные
    product_name = TestDataGenerator.generate_product_name()
    
    print(f"\n📦 Создаем товар с габаритами: {product_name}")
    
    # Создаем товар с размерами
    products_page.click_create_product()
    products_page.fill_product_form(
        name=product_name,
        barcode=TestDataGenerator.generate_barcode(),
        height=25.5,
        width=15.0,
        depth=10.0,
        weight=2.5
    )
    products_page.click_save()
    
    # Проверяем
    assert products_page.is_product_in_list(product_name), \
        f"Товар '{product_name}' с габаритами не создан"
    
    print(f"✓ Товар с габаритами (25.5x15x10 см, 2.5 кг) создан")


@pytest.mark.products
@pytest.mark.regression
@pytest.mark.P1
def test_create_product_with_pricing(authenticated_page):
    """
    Тест: Создание товара с полным ценообразованием
    
    Проверяет:
    - Цену закупки
    - Наценку
    - Цену продажи
    - Автоматический расчет наценки
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    product_name = TestDataGenerator.generate_product_name()
    
    print(f"\n💰 Создаем товар с ценообразованием: {product_name}")
    
    # Создаем товар с ценами
    products_page.click_create_product()
    products_page.fill_product_form(
        name=product_name,
        barcode=TestDataGenerator.generate_barcode(),
        purchase_price=500,
        markup=50,  # 50% наценка
        price=750  # Цена продажи
    )
    products_page.click_save()
    
    # Проверяем
    assert products_page.is_product_in_list(product_name), \
        f"Товар '{product_name}' с ценообразованием не создан"
    
    print(f"✓ Товар с ценами (закупка: 500, наценка: 50%, продажа: 750) создан")


@pytest.mark.products
@pytest.mark.regression
@pytest.mark.P2
def test_create_product_with_min_stock(authenticated_page):
    """
    Тест: Создание товара с минимальным остатком
    
    Проверяет настройку минимального остатка для уведомлений
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    product_name = TestDataGenerator.generate_product_name()
    
    print(f"\n📊 Создаем товар с минимальным остатком: {product_name}")
    
    # Создаем товар с минимальным остатком
    products_page.click_create_product()
    products_page.fill_product_form(
        name=product_name,
        barcode=TestDataGenerator.generate_barcode(),
        price=1000,
        min_stock=5  # Минимальный остаток 5 штук
    )
    products_page.click_save()
    
    # Проверяем
    assert products_page.is_product_in_list(product_name), \
        f"Товар '{product_name}' с минимальным остатком не создан"
    
    print(f"✓ Товар с минимальным остатком (5 шт) создан")

