"""
Тесты для авторизации на CloudShop и работы с товарами
"""

import pytest
import os
from playwright.sync_api import sync_playwright, expect
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


def test_login_and_create_product():
    """
    Тест: Авторизация на CloudShop и создание товара
    
    Шаги:
    1. Открыть страницу авторизации
    2. Ввести email и пароль
    3. Войти в систему
    4. Перейти в раздел "Товары и услуги"
    5. Нажать кнопку "Создать товар" (если есть баннер - закрыть его)
    6. Заполнить все обязательные поля
    7. Нажать кнопку "Сохранить"
    8. Проверить успешное создание
    """
    with sync_playwright() as playwright:
        # Запускаем браузер с параметрами для стабильности (на весь экран)
        browser = playwright.chromium.launch(
            headless=False,  # Для визуального запуска
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)  # На весь экран
        page = context.new_page()
        
        try:
            # Получаем учетные данные из переменных окружения
            email = os.getenv("CLOUDSHOP_EMAIL")
            password = os.getenv("CLOUDSHOP_PASSWORD")
            
            if not email or not password:
                pytest.skip("Учетные данные не найдены в .env файле")
            
            # Шаг 1: Открываем страницу авторизации
            page.goto("https://web.cloudshop.ru/anonymous/login/")
            expect(page).to_have_title("Авторизация", timeout=10000)
            print("✓ Страница авторизации открыта")
            
            # Шаг 2-3: Авторизация
            page.fill('input[placeholder*="Email"][type="text"], input[name*="email"], input[type="email"]', email)
            page.fill('input[placeholder*="Пароль"][type="password"], input[name*="password"]', password)
            page.click('button:has-text("войти"), button[type="submit"]:has-text("войти")')
            print("✓ Авторизация выполнена")
            
            # Ждем загрузки после авторизации
            page.wait_for_timeout(3000)
            print("✓ Дождались загрузки после авторизации")
            
            # Шаг 4: Переход в раздел "Товары и услуги"
            page.goto("https://web.cloudshop.ru/card/catalog/list")
            page.wait_for_timeout(3000)
            assert "/card/catalog/list" in page.url, f"Ожидался переход на страницу товаров, текущий URL: {page.url}"
            print("✓ Перешли в раздел 'Товары и услуги'")
            
            # Шаг 5: Нажимаем кнопку "Создать товар"
            print("\nИщем кнопку 'Создать товар'...")
            
            # Сначала пытаемся кликнуть на кнопку "Создать товар"
            try:
                create_button = page.locator('a:has-text("Создать товар"), button:has-text("Создать товар")')
                if create_button.count() > 0:
                    create_button.first.click()
                    print("✓ Клик по кнопке 'Создать товар' выполнен")
                else:
                    print("⚠ Кнопка 'Создать товар' не найдена")
            except Exception as e:
                print(f"⚠ Ошибка при клике на 'Создать товар': {e}")
            
            # Ждем немного, возможно появится баннер
            page.wait_for_timeout(2000)
            
            # Проверяем наличие всплывающего баннера и закрываем его
            try:
                # Ищем кнопку "Закрыть" в баннере
                close_buttons = page.locator('text="Закрыть", button:has-text("Закрыть"), a:has-text("Закрыть")')
                if close_buttons.count() > 0:
                    # Фильтруем только видимые элементы
                    for i in range(close_buttons.count()):
                        close_btn = close_buttons.nth(i)
                        if close_btn.is_visible():
                            close_btn.click()
                            print("✓ Баннер закрыт")
                            page.wait_for_timeout(1000)
                            
                            # После закрытия баннера снова пытаемся кликнуть "Создать товар"
                            try:
                                create_button = page.locator('a:has-text("Создать товар"), button:has-text("Создать товар")')
                                if create_button.count() > 0:
                                    create_button.first.click()
                                    print("✓ Повторный клик по кнопке 'Создать товар' выполнен")
                            except:
                                pass
                            break
            except:
                pass
            
            # Ждем загрузки формы создания товара
            page.wait_for_timeout(3000)
            print("✓ Ждем загрузки формы создания товара")
            
            # Проверяем, что мы на странице создания товара (может быть модальное окно)
            current_url = page.url
            assert "/create/" in current_url, f"Ожидалась форма создания товара, текущий URL: {current_url}"
            print("✓ Форма создания товара открыта")
            print(f"   URL: {current_url}")
            
            # Шаг 6: Заполнение полей товара в модальном окне справа
            print("\nЗаполняем поля товара в модальном окне...")
            page.wait_for_timeout(3000)  # Даем больше времени на загрузку модального окна
            
            # Ищем модальное окно или сайдбар справа
            modal_selector = '.cs.sidebar, .modal, .ui.sidebar, [ui-view="modal"]'
            modal = page.locator(modal_selector).first
            
            if modal.count() > 0 and modal.is_visible():
                print("✓ Модальное окно найдено")
                # Кликаем по модальному окну для фокуса
                modal.click()
                page.wait_for_timeout(500)
            
            # Ищем поле "Наименование" в модальном окне (не в поисковой строке)
            try:
                # Пробуем найти поле по label или placeholder
                name_input = page.locator('.cs.sidebar input[placeholder*="Наимен"], .modal input[placeholder*="Наимен"], [ui-view="modal"] input[placeholder*="Наимен"]').first
                if name_input.is_visible() and not name_input.is_disabled():
                    name_input.fill("Тестовый товар автоматизации")
                    print("✓ Наименование товара заполнено: 'Тестовый товар автоматизации'")
                else:
                    # Альтернативный поиск - ищем input который НЕ в поисковой строке
                    all_text_inputs = page.locator('.cs.sidebar input[type="text"], [ui-view="modal"] input[type="text"]')
                    if all_text_inputs.count() > 1:
                        # Пропускаем первое поле (поисковая строка), берем второе
                        name_input = all_text_inputs.nth(1)
                        if name_input.is_visible() and not name_input.is_disabled():
                            name_input.fill("Тестовый товар автоматизации")
                            print("✓ Наименование товара заполнено: 'Тестовый товар автоматизации' (поле 2)")
            except Exception as e:
                print(f"⚠ Ошибка при заполнении наименования: {e}")
            
            # Поле штрих-кода (если доступно)
            try:
                barcode_input = page.locator('input[placeholder="Введите штрих-код"]')
                if barcode_input.is_visible() and not barcode_input.is_disabled():
                    barcode_input.fill("1234567890123")
                    print("✓ Штрих-код заполнен")
            except:
                pass
            
            # Поле артикула (если доступно)
            try:
                article_input = page.locator('input[placeholder="Введите артикул"]')
                if article_input.is_visible() and not article_input.is_disabled():
                    article_input.fill("ART-001")
                    print("✓ Артикул заполнен: 'ART-001'")
            except:
                pass
            
            # Поля с числовыми значениями (цены)
            try:
                price_inputs = page.locator('input[type="number"]')
                if price_inputs.count() > 0:
                    filled_count = 0
                    for i in range(min(3, price_inputs.count())):
                        try:
                            price_inp = price_inputs.nth(i)
                            if price_inp.is_visible() and not price_inp.is_disabled():
                                price_inp.fill("1000")
                                filled_count += 1
                                print(f"✓ Цена заполнена: 1000 (поле {filled_count})")
                                if filled_count >= 2:  # Заполняем несколько полей
                                    break
                        except:
                            continue
            except:
                pass
            
            # Текстовое поле описания (textarea)
            try:
                description_textarea = page.locator('textarea')
                if description_textarea.is_visible() and not description_textarea.is_disabled():
                    description_textarea.fill("Тестовый товар автоматизации - создан Playwright")
                    print("✓ Описание заполнено")
            except:
                pass
            
            # Ждем немного, чтобы кнопка "Сохранить" появилась
            page.wait_for_timeout(2000)
            print("\nИщем кнопку 'Сохранить' или 'Создать'...")
            
            # Шаг 7: Нажимаем кнопку "Сохранить" в модальном окне
            print("\nИщем кнопку 'Сохранить' в модальном окне...")
            
            # Ищем кнопку "Сохранить" по селектору
            try:
                save_button = page.locator('.cs.sidebar a.ui.button.green:has-text("Сохранить"), [ui-view="modal"] a.ui.button.green:has-text("Сохранить")')
                if save_button.count() > 0:
                    save_button.first.click()
                    print("✓ Клик по кнопке 'Сохранить' выполнен")
                else:
                    print("⚠ Кнопка не найдена через Playwright, пробуем JavaScript...")
                    raise Exception("Не найдена через Playwright")
            except:
                # Альтернатива через JavaScript
                result = page.evaluate("""
                    () => {
                        const modal = document.querySelector('.cs.sidebar, [ui-view="modal"]');
                        const buttons = Array.from(modal.querySelectorAll('a.ui.button.green'));
                        for (let btn of buttons) {
                            if (btn.innerText.trim().toLowerCase().includes('сохранить')) {
                                btn.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
                
                if result:
                    print("✓ Клик по кнопке выполнен через JavaScript")
                else:
                    print("⚠ Кнопка не найдена, пытаемся любой зеленой кнопкой...")
                    page.locator('[ui-view="modal"] a.ui.button.green').first.click()
                    print("✓ Клик по зеленой кнопке выполнен")
            
            # Ждем сохранения и закрытия модального окна
            print("\nЖдем сохранения товара...")
            page.wait_for_timeout(5000)
            
            # Шаг 8: Проверка успешного создания - ищем товар в таблице
            print("\nПроверяем, создался ли товар...")
            
            # Переходим на страницу списка товаров (если еще не там)
            if "/card/catalog/list" not in page.url:
                page.goto("https://web.cloudshop.ru/card/catalog/list")
                page.wait_for_timeout(3000)
            
            # Ищем созданный товар в таблице
            product_name = "Тестовый товар автоматизации"
            found = page.evaluate(f"""
                (name) => {{
                    // Ищем товар по тексту в таблице
                    const cells = Array.from(document.querySelectorAll('td, div'));
                    for (let cell of cells) {{
                        if (cell.innerText.includes(name)) {{
                            return true;
                        }}
                    }}
                    return false;
                }}
            """, product_name)
            
            if found:
                print("✓✓✓ ТОВАР УСПЕШНО СОЗДАН И НАЙДЕН В ТАБЛИЦЕ! ✓✓✓")
                print(f"✓ Товар '{product_name}' присутствует в списке товаров")
            else:
                # Проверяем, появился ли хотя бы новый товар
                print("⚠ Товар с точным названием не найден, проверяем общее количество...")
                # Делаем скриншот для отладки
                page.screenshot(path="screenshot_products_list.png")
                print("⚠ Скриншот сохранен: screenshot_products_list.png")
            
            # Проверяем URL
            current_url = page.url
            print(f"✓ Финальный URL: {current_url}")
            
            # Финальная проверка
            assert found, f"Товар '{product_name}' не найден в таблице после создания"
            
            print("\n✓✓✓ ТЕСТ УСПЕШНО ЗАВЕРШЕН! ✓✓✓")
            
        except Exception as e:
            print(f"\n✗✗✗ ОШИБКА: {str(e)} ✗✗✗")
            # Делаем скриншот при ошибке
            page.screenshot(path="screenshot_error.png")
            import traceback
            traceback.print_exc()
            raise
        
        finally:
            # Закрываем браузер
            print("\nЗакрываем браузер...")
            context.close()
            browser.close()
