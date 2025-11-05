import pytest
from playwright.sync_api import sync_playwright, expect


def test_open_cloudshop_page():
    """
    Тест на открытие главной страницы cloudshop.ru
    """
    with sync_playwright() as playwright:
        # Запускаем браузер с параметрами для стабильности
        browser = playwright.chromium.launch(
            headless=False,  # Для визуального запуска (можно изменить на True)
            args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
        )
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            # Открываем страницу
            page.goto("https://cloudshop.ru")
            
            # Проверяем, что страница загрузилась (проверяем заголовок содержит "CloudShop")
            title = page.title()
            assert "CloudShop" in title, f"Заголовок должен содержать 'CloudShop', получен: {title}"
            
            # Проверяем, что URL корректный
            # expect(page).to_have_url("https://cloudshop.ru/")
            
            # Проверяем, что есть какой-то контент на странице
            # (например, проверяем наличие элемента навигации или логотипа)
            page.wait_for_load_state("networkidle")
            
            print("Страница cloudshop.ru успешно открыта!")

            # Кликаем по кнопке "Вход"
            page.locator("button:has-text('ВХОД')").click()
            
        finally:
            # Закрываем браузер
            context.close()
            browser.close()

