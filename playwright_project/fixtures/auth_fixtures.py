"""
Fixtures для авторизации
"""

import pytest
import os
from dotenv import load_dotenv
from pages.login_page import LoginPage

load_dotenv()


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
    load_dotenv()
    return {
        "email": os.getenv("CLOUDSHOP_EMAIL"),
        "password": os.getenv("CLOUDSHOP_PASSWORD")
    }

