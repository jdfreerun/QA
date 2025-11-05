"""
Базовый класс для всех Page Objects
"""

from playwright.sync_api import Page


class BasePage:
    """Базовый класс страницы с общими методами"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        """Переход на URL"""
        self.page.goto(url)
    
    def click(self, locator: str, timeout: int = 30000):
        """Клик по элементу"""
        self.page.click(locator, timeout=timeout)
    
    def fill(self, locator: str, value: str, timeout: int = 30000):
        """Заполнение поля"""
        self.page.fill(locator, value, timeout=timeout)
    
    def get_text(self, locator: str) -> str:
        """Получение текста элемента"""
        return self.page.locator(locator).inner_text()
    
    def is_visible(self, locator: str) -> bool:
        """Проверка видимости элемента"""
        return self.page.locator(locator).is_visible()
    
    def wait_for_load(self, timeout: int = 3000):
        """Ожидание загрузки"""
        self.page.wait_for_timeout(timeout)
    
    def wait_for_element(self, locator: str, timeout: int = 10000):
        """Ожидание появления элемента"""
        self.page.wait_for_selector(locator, timeout=timeout)
    
    def get_current_url(self) -> str:
        """Получение текущего URL"""
        return self.page.url
    
    def screenshot(self, path: str):
        """Создание скриншота"""
        self.page.screenshot(path=path)

