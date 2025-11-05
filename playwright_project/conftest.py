"""
Конфигурация pytest и общие fixtures
"""

import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from pages.login_page import LoginPage

load_dotenv()


@pytest.fixture(scope="session")
def playwright_instance():
    """Playwright instance для всей сессии"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Браузер для всей сессии"""
    browser = playwright_instance.chromium.launch(
        headless=False,  # Можно изменить на True для headless режима
        args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage", "--start-maximized"]
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """Контекст браузера для каждого теста"""
    context = browser.new_context(no_viewport=True)  # На весь экран
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Новая страница для каждого теста"""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def authenticated_page(page):
    """
    Фикстура для авторизованной сессии
    
    Возвращает страницу с уже выполненной авторизацией
    """
    login_page = LoginPage(page)
    login_page.open()
    
    email = os.getenv("CLOUDSHOP_EMAIL")
    password = os.getenv("CLOUDSHOP_PASSWORD")
    
    if not email or not password:
        pytest.skip("Учетные данные не найдены в .env файле")
    
    login_page.login(email, password)
    
    # Проверяем успешность авторизации
    assert login_page.is_login_successful(), "Авторизация не выполнена"
    
    return page


@pytest.fixture(scope="function")
def login_credentials():
    """
    Получение учетных данных из .env
    
    Returns:
        dict: {"email": "...", "password": "..."}
    """
    return {
        "email": os.getenv("CLOUDSHOP_EMAIL"),
        "password": os.getenv("CLOUDSHOP_PASSWORD")
    }


@pytest.fixture(scope="function")
def test_product_data():
    """Генерирует данные для тестового товара"""
    from utils.data_generator import TestDataGenerator
    return TestDataGenerator.generate_product_data()


# Хуки pytest для улучшения отчетности
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания скриншота при падении теста
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Пытаемся получить page из теста
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                screenshot_name = f"screenshot_fail_{item.name}.png"
                page.screenshot(path=screenshot_name)
                print(f"\n📸 Скриншот сохранен: {screenshot_name}")
            except:
                pass

