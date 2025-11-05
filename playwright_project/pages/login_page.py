"""
Page Object для страницы авторизации
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    """Страница авторизации CloudShop"""
    
    # Локаторы
    EMAIL_INPUT = 'input[placeholder*="Email"][type="text"], input[name*="email"], input[type="email"]'
    PASSWORD_INPUT = 'input[placeholder*="Пароль"][type="password"], input[name*="password"]'
    LOGIN_BUTTON = 'button:has-text("войти"), button[type="submit"]:has-text("войти")'
    FORGOT_PASSWORD_LINK = 'a:has-text("Забыли пароль?")'
    REGISTER_LINK = 'a:has-text("Регистрация")'
    QR_CODE_BUTTON = 'text="Войти по QR-коду"'
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://web.cloudshop.ru/anonymous/login/"
    
    def open(self):
        """Открыть страницу авторизации"""
        self.navigate(self.url)
        self.wait_for_load(2000)
    
    def login(self, email: str, password: str):
        """
        Авторизация пользователя
        
        Args:
            email: Email пользователя
            password: Пароль пользователя
        """
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_load(3000)
    
    def is_login_successful(self) -> bool:
        """Проверка успешной авторизации"""
        return "/anonymous/login" not in self.get_current_url()
    
    def click_forgot_password(self):
        """Клик по ссылке 'Забыли пароль?'"""
        self.click(self.FORGOT_PASSWORD_LINK)
    
    def click_register(self):
        """Клик по ссылке 'Регистрация'"""
        self.click(self.REGISTER_LINK)

