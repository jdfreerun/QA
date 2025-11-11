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
    
    print(f"\n✏️ Редактируем товар на: {new_name}")
    
    # Кликаем по строке
    products_page.click_product_row(original_name)
    
    # Нажимаем "Редактировать"
    products_page.click_edit_button()
    
    # Обновляем поля
    # Очищаем и заполняем название
    modal_inputs = authenticated_page.locator('[ui-view="modal"] input[type="text"]')
    if modal_inputs.count() > 1:
        name_input = modal_inputs.nth(1)
        name_input.fill("")  # Очищаем
        name_input.fill(new_name)
        print(f"  ✓ Новое название: {new_name}")
    
    # Обновляем цену
    price_input = authenticated_page.locator('.field:has-text("Цена продажи") input[type="number"]').first
    if price_input.count() > 0:
        authenticated_page.evaluate("""
            () => {
                const modal = document.querySelector('.cs.sidebar, [ui-view="modal"]');
                modal.scrollTop = modal.scrollHeight;
            }
        """)
        authenticated_page.wait_for_timeout(500)
        price_input.scroll_into_view_if_needed()
        price_input.fill(str(new_price))
        print(f"  ✓ Новая цена: {new_price}")
    
    # Сохраняем
    products_page.click_save()
    
    # Проверяем обновление
    assert products_page.is_product_in_list(new_name), \
        f"Товар '{new_name}' не найден после редактирования"
    
    print(f"\n✓✓✓ Товар успешно отредактирован! ✓✓✓")

