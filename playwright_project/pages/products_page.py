"""
Page Object для страницы товаров
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class ProductsPage(BasePage):
    """Страница управления товарами и услугами"""
    
    # Локаторы
    CREATE_BUTTON = 'a:has-text("Создать товар"), button:has-text("Создать товар")'
    SEARCH_INPUT = 'input[type="text"][placeholder*="поиск"], input[type="text"]:first-child, input.search'
    CLOSE_BANNER_BUTTON = 'text="Закрыть", button:has-text("Закрыть"), a:has-text("Закрыть")'
    
    # Локаторы модального окна создания
    MODAL_SELECTOR = '.cs.sidebar, [ui-view="modal"]'
    MODAL_NAME_INPUT = '[ui-view="modal"] input[type="text"]'
    MODAL_BARCODE_INPUT = 'input[placeholder="Введите штрих-код"]'
    MODAL_ARTICLE_INPUT = 'input[placeholder="Введите артикул"]'
    MODAL_PRICE_INPUT = 'input[type="number"]'
    MODAL_DESCRIPTION_TEXTAREA = 'input[placeholder="Описание"]'
    SAVE_BUTTON = '.cs.sidebar a.ui.button.green:has-text("Сохранить"), [ui-view="modal"] a.ui.button.green:has-text("Сохранить")'
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://web.cloudshop.ru/card/catalog/list"
    
    def open(self):
        """Открыть страницу товаров"""
        self.navigate(self.url)
        self.wait_for_load(3000)
    
    def click_create_product(self):
        """Клик по кнопке создания товара"""
        self.click(self.CREATE_BUTTON)
        self.wait_for_load(2000)
        
        # Закрываем баннер если появился
        self._close_banner_if_exists()
    
    def _close_banner_if_exists(self):
        """Закрыть всплывающий баннер если есть"""
        try:
            close_buttons = self.page.locator(self.CLOSE_BANNER_BUTTON)
            if close_buttons.count() > 0:
                for i in range(close_buttons.count()):
                    close_btn = close_buttons.nth(i)
                    if close_btn.is_visible():
                        close_btn.click()
                        self.wait_for_load(1000)
                        break
        except:
            pass
    
    def fill_product_form(self, name: str, barcode: str = None, article: str = None, 
                         price: int = None, description: str = None, 
                         unit: str = None, category: str = None, country: str = None,
                         purchase_price: int = None, markup: int = None,
                         weight: float = None, height: float = None, 
                         width: float = None, depth: float = None,
                         min_stock: int = None, tax_code: str = None):
        """
        Заполнение формы создания товара (расширенная версия)
        
        Args:
            name: Название товара (обязательное)
            barcode: Штрих-код
            article: Артикул
            price: Цена продажи
            description: Описание
            unit: Единица измерения
            category: Категория
            country: Страна
            purchase_price: Цена закупки
            markup: Наценка (%)
            weight: Вес в кг
            height: Высота в см
            width: Ширина в см
            depth: Глубина в см
            min_stock: Минимальный остаток
            tax_code: Код налога
        """
        # Кликаем по модальному окну для фокуса
        modal = self.page.locator(self.MODAL_SELECTOR).first
        if modal.count() > 0 and modal.is_visible():
            modal.click()
            self.wait_for_load(500)
        
        # Заполняем название (пропускаем первое поле - это поиск)
        all_text_inputs = self.page.locator(self.MODAL_NAME_INPUT)
        if all_text_inputs.count() > 1:
            all_text_inputs.nth(1).fill(name)
            print(f"  ✓ Наименование: {name}")
        
        # Штрих-код
        if barcode:
            try:
                barcode_input = self.page.locator(self.MODAL_BARCODE_INPUT)
                if barcode_input.is_visible() and not barcode_input.is_disabled():
                    barcode_input.fill(barcode)
                    print(f"  ✓ Штрих-код: {barcode}")
            except:
                pass
        
        # Артикул
        if article:
            try:
                article_input = self.page.locator(self.MODAL_ARTICLE_INPUT)
                if article_input.is_visible() and not article_input.is_disabled():
                    article_input.fill(article)
                    print(f"  ✓ Артикул: {article}")
            except:
                pass
        
        # Единица измерения (необязательное поле, пропускаем)
        # TODO: Поле не обязательное, требует доработки для корректного выбора
        if unit:
            print(f"  ⚠ Единица измерения: пропущено (необязательное поле)")
        
        # Описание
        if description:
            try:
                desc_textarea = self.page.locator(self.MODAL_DESCRIPTION_TEXTAREA)
                if desc_textarea.is_visible() and not desc_textarea.is_disabled():
                    desc_textarea.fill(description)
                    print(f"  ✓ Описание заполнено")
            except:
                pass
        
        # Страна (необязательное поле, пропускаем)
        # TODO: Поле не обязательное, требует доработки для корректного выбора
        if country:
            print(f"  ⚠ Страна: пропущено (необязательное поле)")
        
        # Прокручиваем еще ниже для цен
        self.page.evaluate("""
            () => {
                const modal = document.querySelector('.cs.sidebar, [ui-view="modal"]');
                if (modal) {
                    modal.scrollTop = modal.scrollHeight;
                }
            }
        """)
        self.wait_for_load(500)
        
        # Цена закупки
        if purchase_price:
            try:
                purchase_input = self.page.locator('.field:has-text("Цена закупки") input[type="number"]').first
                if purchase_input.count() > 0:
                    purchase_input.scroll_into_view_if_needed()
                    self.wait_for_load(300)
                    purchase_input.fill(str(purchase_price))
                    print(f"  ✓ Цена закупки: {purchase_price}")
            except Exception as e:
                print(f"  ⚠ Цена закупки не заполнена: {e}")
        
        # Наценка
        if markup:
            try:
                markup_input = self.page.locator('.field:has-text("Наценка") input[type="number"]').first
                if markup_input.count() > 0:
                    markup_input.scroll_into_view_if_needed()
                    self.wait_for_load(300)
                    markup_input.fill(str(markup))
                    print(f"  ✓ Наценка: {markup}%")
            except Exception as e:
                print(f"  ⚠ Наценка не заполнена: {e}")
        
        # Цена продажи
        if price:
            try:
                price_input = self.page.locator('.field:has-text("Цена продажи") input[type="number"]').first
                if price_input.count() > 0:
                    price_input.scroll_into_view_if_needed()
                    self.wait_for_load(300)
                    price_input.fill(str(price))
                    print(f"  ✓ Цена продажи: {price}")
            except Exception as e:
                print(f"  ⚠ Цена продажи не заполнена: {e}")
        
        # Размеры (если указаны)
        if height:
            try:
                height_input = self.page.locator('.field:has-text("Высота") input[type="number"]').first
                if height_input.count() > 0:
                    height_input.scroll_into_view_if_needed()
                    self.wait_for_load(300)
                    height_input.fill(str(height))
                    print(f"  ✓ Высота: {height} см")
            except Exception as e:
                print(f"  ⚠ Высота не заполнена: {e}")
        
        if width:
            try:
                width_input = self.page.locator('.field:has-text("Ширина") input[type="number"]').first
                if width_input.count() > 0:
                    width_input.scroll_into_view_if_needed()
                    self.wait_for_load(300)
                    width_input.fill(str(width))
                    print(f"  ✓ Ширина: {width} см")
            except Exception as e:
                print(f"  ⚠ Ширина не заполнена: {e}")
        
        if depth:
            try:
                depth_input = self.page.locator('.field:has-text("Глубина") input[type="number"]').first
                if depth_input.count() > 0:
                    depth_input.scroll_into_view_if_needed()
                    self.wait_for_load(300)
                    depth_input.fill(str(depth))
                    print(f"  ✓ Глубина: {depth} см")
            except Exception as e:
                print(f"  ⚠ Глубина не заполнена: {e}")
        
        if weight:
            try:
                weight_input = self.page.locator('.field:has-text("вес") input[type="number"]').first
                if weight_input.count() > 0:
                    weight_input.scroll_into_view_if_needed()
                    self.wait_for_load(300)
                    weight_input.fill(str(weight))
                    print(f"  ✓ Вес: {weight} кг")
            except Exception as e:
                print(f"  ⚠ Вес не заполнен: {e}")
        
        # Минимальный остаток
        if min_stock:
            try:
                min_stock_input = self.page.locator('.field:has-text("Минимальный остаток") input[type="number"]').first
                if min_stock_input.count() > 0:
                    min_stock_input.scroll_into_view_if_needed()
                    self.wait_for_load(300)
                    min_stock_input.fill(str(min_stock))
                    print(f"  ✓ Минимальный остаток: {min_stock}")
            except Exception as e:
                print(f"  ⚠ Минимальный остаток не заполнен: {e}")
        
        # Код налога (необязательное поле, пропускаем)
        # TODO: Поле не обязательное, требует доработки для корректного выбора
        if tax_code:
            print(f"  ⚠ Код налога: пропущено (необязательное поле)")
        
        self.wait_for_load(1000)
    
    def click_save(self):
        """Нажать кнопку 'Сохранить'"""
        try:
            save_button = self.page.locator(self.SAVE_BUTTON)
            if save_button.count() > 0:
                save_button.first.click()
            else:
                # JavaScript клик как запасной вариант
                self.page.evaluate("""
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
        except Exception as e:
            raise Exception(f"Не удалось нажать кнопку 'Сохранить': {e}")
        
        self.wait_for_load(5000)
    
    def create_product(self, name: str, **kwargs):
        """
        Полный цикл создания товара
        
        Args:
            name: Название товара
            **kwargs: Дополнительные поля (barcode, article, price, description)
        """
        self.click_create_product()
        self.fill_product_form(name, **kwargs)
        self.click_save()
    
    def search_product(self, product_name: str):
        """Поиск товара по названию"""
        self.fill(self.SEARCH_INPUT, product_name)
        self.wait_for_load(1000)
    
    def is_product_in_list(self, product_name: str) -> bool:
        """
        Проверка наличия товара в списке
        
        Args:
            product_name: Название товара для поиска
            
        Returns:
            True если товар найден, False если нет
        """
        return self.page.evaluate("""
            (name) => {
                const cells = Array.from(document.querySelectorAll('td, div, span'));
                return cells.some(cell => cell.innerText.includes(name));
            }
        """, product_name)
    
    def get_products_count(self) -> int:
        """Получить количество товаров в списке"""
        # Подсчет строк в таблице товаров
        rows = self.page.locator('table tbody tr, .product-row')
        return rows.count()
    
    def delete_product(self, product_name: str):
        """Удаление товара"""
        # Найти товар и кликнуть по кнопке удаления
        # TODO: реализовать после изучения UI
        pass
    
    def edit_product(self, product_name: str):
        """Редактирование товара"""
        # Найти товар и открыть на редактирование
        # TODO: реализовать после изучения UI
        pass

