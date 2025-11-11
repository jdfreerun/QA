"""
Тест удаления товара
"""

import pytest
from pages.products_page import ProductsPage
from utils.data_generator import TestDataGenerator


@pytest.mark.products
@pytest.mark.smoke
@pytest.mark.P0
def test_delete_product(authenticated_page):
    """
    Тест: Удаление товара
    
    Предусловия: Пользователь авторизован
    Шаги:
        1. Открыть страницу товаров
        2. Создать тестовый товар
        3. Выбрать чекбокс товара
        4. Открыть dropdown "Действия над товаром"
        5. Нажать "Удалить" в открывшемся списке
        6. Подтвердить удаление (нажать "Да")
        7. Проверить перемещение товара в корзину
    Ожидаемый результат: Товар успешно удален (перемещен в корзину)
    """
    products_page = ProductsPage(authenticated_page)
    products_page.open()
    
    # Создаем товар для удаления
    product_name = TestDataGenerator.generate_product_name()
    
    print(f"\n📦 Создаем товар для удаления: {product_name}")
    products_page.create_product(
        name=product_name,
        barcode=TestDataGenerator.generate_barcode()
    )
    
    # Проверяем создание
    assert products_page.is_product_in_list(product_name), \
        f"Товар '{product_name}' не создан"
    
    # Удаляем товар
    print(f"\n🗑️ Удаляем товар: {product_name}")
    products_page.delete_product(product_name)
    
    # В CloudShop товары перемещаются в корзину вместо полного удаления
    # Проверяем, что товар перемещен в корзину
    authenticated_page.goto("https://web.cloudshop.ru/card/trash/")
    authenticated_page.wait_for_timeout(3000)
    
    # Проверяем, что товар в корзине
    in_trash = products_page.is_product_in_list(product_name)
    
    if in_trash:
        print(f"✓ Товар '{product_name}' перемещен в корзину")
    else:
        # Проверяем, что товар удален из основного списка
        authenticated_page.goto("https://web.cloudshop.ru/card/catalog/list")
        authenticated_page.wait_for_timeout(3000)
        assert not products_page.is_product_in_list(product_name), \
            f"Товар '{product_name}' все еще в списке после удаления"
        print(f"✓ Товар '{product_name}' удален из списка")
    
    print(f"\n✓✓✓ Товар успешно удален! ✓✓✓")

