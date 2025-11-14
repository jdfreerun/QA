"""
Тест редактирования товара
"""

import pytest
from pages.products_page import ProductsPage
from utils.data_generator import TestDataGenerator


@pytest.mark.products
@pytest.mark.smoke
@pytest.mark.P0
def test_edit_product(authenticated_page):
    """
    Тест: Редактирование товара
    
    Предусловия: Пользователь авторизован
    Шаги:
        1. Открыть страницу товаров
        2. Создать тестовый товар
        3. Кликнуть по строке товара для открытия карточки
        4. Нажать "Редактировать" в модальном окне
        5. Изменить поля товара (название и цену)
        6. Сохранить изменения
        7. Проверить обновление
    Ожидаемый результат: Товар успешно отредактирован
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Создаем товар
    original_name = TestDataGenerator.generate_product_name()
    original_price = 1000
    
    print(f"\n📦 Создаем товар: {original_name}")
    products_page.create_product(
        name=original_name,
        barcode=TestDataGenerator.generate_barcode(),
        price=original_price
    )
    
    # Проверяем создание
    assert products_page.is_product_in_list(original_name), \
        f"Товар '{original_name}' не создан"
    
    # Редактируем товар
    new_name = original_name + " (EDITED)"
    new_price = 2000
    
    print(f"\n✏️ Редактируем товар:")
    print(f"   Старое название: {original_name}")
    print(f"   Новое название: {new_name}")
    print(f"   Старая цена: {original_price}")
    print(f"   Новая цена: {new_price}")
    
    # Используем метод edit_product из ProductsPage
    products_page.edit_product(
        product_name=original_name,
        name=new_name,
        price=new_price
    )
    
    # Проверяем обновление
    assert products_page.is_product_in_list(new_name), \
        f"Товар '{new_name}' не найден после редактирования"
    
    print(f"\n✓✓✓ Товар успешно отредактирован! ✓✓✓")

