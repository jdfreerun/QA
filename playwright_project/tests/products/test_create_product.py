"""
Тест создания товара с заполнением всех полей
"""

import pytest
from pages.products_page import ProductsPage
from utils.data_generator import TestDataGenerator


@pytest.mark.products
@pytest.mark.smoke
@pytest.mark.P0
def test_create_product_with_all_fields(authenticated_page):
    """
    Тест: Создание товара с заполнением всех доступных полей
    
    Предусловия: Пользователь авторизован
    Шаги:
        1. Открыть страницу "Товары и услуги"
        2. Нажать "Создать товар"
        3. Заполнить все доступные поля в модальном окне
        4. Нажать "Сохранить"
        5. Проверить наличие товара в списке
    Ожидаемый результат: Товар создан и отображается в списке
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Генерируем полный набор данных
    product_data = TestDataGenerator.generate_product_data(full=True)
    
    print(f"\n📦 Создаем товар с полным набором полей:")
    print(f"   Название: {product_data['name']}")
    print(f"   Штрих-код: {product_data['barcode']}")
    print(f"   Артикул: {product_data['article']}")
    
    # Создаем товар
    products_page.click_create_product()
    products_page.fill_product_form(
        name=product_data["name"],
        barcode=product_data["barcode"],
        article=product_data["article"],
        price=product_data["price"],
        description=product_data["description"],
        unit=product_data["unit"],
        country=product_data["country"],
        purchase_price=product_data["purchase_price"],
        markup=product_data["markup"],
        weight=product_data["weight"],
        height=product_data["height"],
        width=product_data["width"],
        depth=product_data["depth"],
        min_stock=product_data["min_stock"],
        tax_code=product_data["tax_code"]
    )
    products_page.click_save()
    
    # Проверяем создание
    assert products_page.is_product_in_list(product_data["name"]), \
        f"Товар '{product_data['name']}' не найден в списке после создания"
    
    print(f"\n✓✓✓ Товар '{product_data['name']}' успешно создан со всеми полями! ✓✓✓")

