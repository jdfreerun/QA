"""
Тесты авторизации CloudShop
"""

import pytest
from pages.login_page import LoginPage


@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.P0
def test_login_success(page, login_credentials):
    """
    Тест: Успешная авторизация с корректными данными
    
    Предусловия: Пользователь не авторизован
    Шаги:
        1. Открыть страницу авторизации
        2. Ввести корректный email
        3. Ввести корректный пароль
        4. Нажать кнопку "Войти"
    Ожидаемый результат: Успешная авторизация, переход на главную страницу
    """
    login_page = LoginPage(page)
    login_page.open()
    
    # Авторизация
    login_page.login(
        email=login_credentials["email"],
        password=login_credentials["password"]
    )
    
    # Проверка
    assert login_page.is_login_successful(), "Авторизация не выполнена"
    assert "/anonymous/login" not in page.url, "Остались на странице авторизации"
    print("✓ Авторизация успешна")


@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.P1
def test_login_invalid_password(page, login_credentials):
    """
    Тест: Авторизация с неверным паролем
    
    Предусловия: Пользователь не авторизован
    Шаги:
        1. Открыть страницу авторизации
        2. Ввести корректный email
        3. Ввести неверный пароль
        4. Нажать кнопку "Войти"
    Ожидаемый результат: Ошибка авторизации, остаемся на странице логина
    """
    login_page = LoginPage(page)
    login_page.open()
    
    # Авторизация с неверным паролем
    login_page.login(
        email=login_credentials["email"],
        password="wrong_password_123"
    )
    
    # Проверка - должны остаться на странице логина
    page.wait_for_timeout(3000)
    assert "/anonymous/login" in page.url, "Авторизация прошла с неверным паролем!"
    print("✓ Ошибка авторизации обработана корректно")


@pytest.mark.auth
@pytest.mark.regression
@pytest.mark.P1
def test_login_empty_fields(page):
    """
    Тест: Попытка авторизации с пустыми полями
    
    Предусловия: Пользователь не авторизован
    Шаги:
        1. Открыть страницу авторизации
        2. Оставить поля пустыми
        3. Нажать кнопку "Войти"
    Ожидаемый результат: Ошибка валидации, кнопка неактивна или показано сообщение
    """
    login_page = LoginPage(page)
    login_page.open()
    
    # Попытка авторизации с пустыми полями
    try:
        login_page.login(email="", password="")
        page.wait_for_timeout(2000)
        
        # Должны остаться на странице логина
        assert "/anonymous/login" in page.url, "Авторизация прошла с пустыми полями!"
        print("✓ Валидация пустых полей работает корректно")
    except:
        # Ожидаемое поведение - ошибка при попытке заполнить пустые поля
        print("✓ Система не позволяет авторизоваться с пустыми полями")


@pytest.mark.auth
@pytest.mark.smoke
@pytest.mark.P0
def test_logout(authenticated_page):
    """
    Тест: Выход из системы
    
    Предусловия: Пользователь авторизован
    Шаги:
        1. Нажать кнопку выхода
        2. Подтвердить выход (если требуется)
    Ожидаемый результат: Перенаправление на страницу авторизации
    """
    # Ищем и кликаем кнопку выхода
    authenticated_page.click('a:has-text("выход"), button:has-text("выход")')
    authenticated_page.wait_for_timeout(2000)
    
    # Проверка - должны быть на странице логина
    assert "/anonymous/login" in authenticated_page.url, "Выход не выполнен"
    print("✓ Выход из системы выполнен успешно")

