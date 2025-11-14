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
    
    # Локаторы модального окна создания/редактирования
    MODAL_SELECTOR = '.cs.sidebar, [ui-view="modal"]'
    MODAL_NAME_INPUT = '[ui-view="modal"] input[type="text"]'
    MODAL_BARCODE_INPUT = 'input[placeholder="Введите штрих-код"]'
    MODAL_ARTICLE_INPUT = 'input[placeholder="Введите артикул"]'
    MODAL_DESCRIPTION_TEXTAREA = 'textarea[ng-model="data.description"]'
    
    # Локаторы цен
    MODAL_PURCHASE_PRICE_INPUT = '.field:has-text("Цена закупки") input[type="number"]'
    MODAL_MARKUP_INPUT = '.field:has-text("Наценка") input[type="number"]'
    MODAL_PRICE_SALE_INPUT = '.field:has-text("Цена продажи") input[type="number"]'
    
    # Локаторы габаритов (используем ng-model для уникальности)
    MODAL_HEIGHT_INPUT = 'input[ng-model="data.size.height_cm"]'
    MODAL_WIDTH_INPUT = 'input[ng-model="data.size.width_cm"]'
    MODAL_DEPTH_INPUT = 'input[ng-model="data.size.depth_cm"]'
    MODAL_WEIGHT_INPUT = 'input[ng-model="data.size.weight_kg"]'
    MODAL_MIN_STOCK_INPUT = '.field:has-text("Минимальный остаток") input[type="number"]'
    
    # ng-model для dropdown'ов с поиском
    # Примечание: единица измерения (unit) не является dropdown'ом
    DROPDOWN_CATEGORY = 'data.categories'  # Категория (multiple selection)
    DROPDOWN_COUNTRY = 'data.country'  # Страна
    DROPDOWN_MARKING_TYPE = 'data.marking_type'  # Тип маркировки
    DROPDOWN_TAX_SYSTEM = 'data.ru_tax_system'  # Система налогообложения
    DROPDOWN_TAXES = 'data.taxes'  # Налоги (multiple selection)
    DROPDOWN_SUPPLIER = 'data.supplier'  # Поставщик
    
    # Локаторы кнопок
    SAVE_BUTTON = '.cs.sidebar a.ui.button.green:has-text("Сохранить"), [ui-view="modal"] a.ui.button.green:has-text("Сохранить")'
    EDIT_BUTTON = 'text="Редактировать"'
    
    # Локаторы для удаления
    ACTIONS_DROPDOWN = 'text="Действия", .dropdown:has-text("Действия"), button:has-text("Действия")'
    DELETE_BUTTON_IN_DROPDOWN = 'div[ng-click="removeSelectedProducts()"], [ng-click*="remove"]'
    CONFIRM_YES_BUTTON = 'text="Да"'
    
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
                         min_stock: int = None, tax_code: str = None,
                         supplier: str = None, taxes: list = None,
                         marking_type: str = None, tax_system: str = None):
        """
        Заполнение формы создания товара (расширенная версия)
        Заполнение происходит по порядку сверху вниз для предотвращения скачков модального окна
        
        Args:
            name: Название товара (обязательное)
            barcode: Штрих-код
            article: Артикул
            price: Цена продажи
            description: Описание
            unit: Единица измерения (не dropdown)
            category: Категория (multiple selection)
            country: Страна
            purchase_price: Цена закупки
            markup: Наценка (%)
            weight: Вес в кг
            height: Высота в см
            width: Ширина в см
            depth: Глубина в см
            min_stock: Минимальный остаток
            tax_code: Код налога
            supplier: Поставщик
            taxes: Список налогов (multiple selection)
            marking_type: Тип маркировки
            tax_system: Система налогообложения
        """
        # Кликаем по модальному окну для фокуса
        modal = self.page.locator(self.MODAL_SELECTOR).first
        if modal.count() > 0 and modal.is_visible():
            modal.click()
            self.wait_for_load(300)
        
        # Заполняем поля без прокруток - используем JavaScript для всех полей
        # 1. Заполняем базовые поля (используют Playwright, но без прокруток)
        self._fill_basic_fields(name, barcode, article, description)
        
        # 2. Заполняем dropdown'ы по порядку (JavaScript - без прокруток в самом методе)
        self._fill_dropdowns_in_order(
            category=category,
            marking_type=marking_type,
            country=country,
            tax_system=tax_system,
            taxes=taxes,
            supplier=supplier
        )
        
        # 3. Цены - заполняем через JavaScript (без прокруток)
        self._fill_pricing(purchase_price, markup, price)
        
        # 4. Габариты - заполняем через JavaScript (без прокруток)
        self._fill_dimensions(height, width, depth, weight)
        
        # 5. Минимальный остаток (только если нужно, через JavaScript)
        if min_stock:
            self._fill_min_stock_optimized(min_stock)
        
        # Код налога (необязательное поле, пропускаем)
        if tax_code:
            print(f"  ⚠ Код налога: пропущено (необязательное поле)")
        
        self.wait_for_load(200)  # Минимальная финальная пауза
    
    def _fill_min_stock_optimized(self, min_stock: int):
        """Оптимизированное заполнение минимального остатка через Playwright API"""
        try:
            min_stock_input = self.page.locator(self.MODAL_MIN_STOCK_INPUT).first
            if min_stock_input.count() > 0:
                # Прокручиваем только если элемент не виден
                if not min_stock_input.is_visible():
                    min_stock_input.scroll_into_view_if_needed(timeout=3000)
                min_stock_input.fill(str(min_stock), timeout=3000)
                print(f"  ✓ Минимальный остаток: {min_stock}")
                self.wait_for_load(100)
        except Exception as e:
            print(f"  ⚠ Минимальный остаток не заполнен: {e}")
    
    def _fill_basic_fields(self, name: str, barcode: str = None, article: str = None, description: str = None):
        """
        Приватный метод для заполнения базовых полей товара
        
        Args:
            name: Название товара (обязательное)
            barcode: Штрих-код
            article: Артикул
            description: Описание
        """
        # Название (пропускаем первое поле - это поиск)
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
        
        # Описание
        if description:
            try:
                desc_textarea = self.page.locator(self.MODAL_DESCRIPTION_TEXTAREA)
                if desc_textarea.is_visible() and not desc_textarea.is_disabled():
                    desc_textarea.fill(description)
                    print(f"  ✓ Описание заполнено")
            except:
                pass
    
    def _fill_pricing(self, purchase_price=None, markup=None, price=None):
        """
        Оптимизированный метод для заполнения цен товара через Playwright API
        Заполняет все поля цен без лишних прокруток
        
        Args:
            purchase_price: Цена закупки
            markup: Наценка в %
            price: Цена продажи
        """
        # Заполняем цены через Playwright API без прокруток
        # Цена закупки
        if purchase_price:
            try:
                purchase_input = self.page.locator(self.MODAL_PURCHASE_PRICE_INPUT).first
                if purchase_input.count() > 0:
                    # Прокручиваем только если элемент не виден
                    if not purchase_input.is_visible():
                        purchase_input.scroll_into_view_if_needed(timeout=3000)
                    purchase_input.fill(str(purchase_price), timeout=3000)
                    print(f"  ✓ Цена закупки: {purchase_price}")
            except Exception as e:
                print(f"  ⚠ Цена закупки не заполнена: {e}")
        
        # Наценка
        if markup:
            try:
                markup_input = self.page.locator(self.MODAL_MARKUP_INPUT).first
                if markup_input.count() > 0:
                    if not markup_input.is_visible():
                        markup_input.scroll_into_view_if_needed(timeout=3000)
                    markup_input.fill(str(markup), timeout=3000)
                    print(f"  ✓ Наценка: {markup}%")
            except Exception as e:
                print(f"  ⚠ Наценка не заполнена: {e}")
        
        # Цена продажи
        if price:
            try:
                price_input = self.page.locator(self.MODAL_PRICE_SALE_INPUT).first
                if price_input.count() > 0:
                    if not price_input.is_visible():
                        price_input.scroll_into_view_if_needed(timeout=3000)
                    price_input.fill(str(price), timeout=3000)
                    print(f"  ✓ Цена продажи: {price}")
            except Exception as e:
                print(f"  ⚠ Цена продажи не заполнена: {e}")
        
        self.wait_for_load(100)  # Минимальная пауза
    
    def _fill_dimensions(self, height=None, width=None, depth=None, weight=None):
        """
        Оптимизированный метод для заполнения габаритов товара через Playwright API
        Заполняет все габариты без лишних прокруток
        
        Args:
            height: Высота в см
            width: Ширина в см
            depth: Глубина в см
            weight: Вес в кг
        """
        # Заполняем все габариты через Playwright API
        # Высота
        if height:
            try:
                height_input = self.page.locator(self.MODAL_HEIGHT_INPUT)
                if height_input.count() > 0:
                    if not height_input.is_visible():
                        height_input.scroll_into_view_if_needed(timeout=3000)
                    height_input.fill(str(height), timeout=3000)
                    print(f"  ✓ Высота: {height} см")
            except Exception as e:
                print(f"  ⚠ Высота не заполнена: {e}")
        
        # Ширина
        if width:
            try:
                width_input = self.page.locator(self.MODAL_WIDTH_INPUT)
                if width_input.count() > 0:
                    if not width_input.is_visible():
                        width_input.scroll_into_view_if_needed(timeout=3000)
                    width_input.fill(str(width), timeout=3000)
                    print(f"  ✓ Ширина: {width} см")
            except Exception as e:
                print(f"  ⚠ Ширина не заполнена: {e}")
        
        # Глубина
        if depth:
            try:
                depth_input = self.page.locator(self.MODAL_DEPTH_INPUT)
                if depth_input.count() > 0:
                    if not depth_input.is_visible():
                        depth_input.scroll_into_view_if_needed(timeout=3000)
                    depth_input.fill(str(depth), timeout=3000)
                    print(f"  ✓ Глубина: {depth} см")
            except Exception as e:
                print(f"  ⚠ Глубина не заполнена: {e}")
        
        # Вес
        if weight:
            try:
                weight_input = self.page.locator(self.MODAL_WEIGHT_INPUT)
                if weight_input.count() > 0:
                    if not weight_input.is_visible():
                        weight_input.scroll_into_view_if_needed(timeout=3000)
                    weight_input.fill(str(weight), timeout=3000)
                    print(f"  ✓ Вес: {weight} кг")
            except Exception as e:
                print(f"  ⚠ Вес не заполнен: {e}")
        
        self.wait_for_load(100)  # Минимальная пауза
    
    def _select_dropdown_by_ng_model(self, ng_model: str, search_text: str = None, field_name: str = None):
        """
        Оптимизированный метод для заполнения dropdown'а по ng-model через Playwright API
        Открывает меню и выбирает первый доступный элемент
        
        Args:
            ng_model: Значение ng-model атрибута dropdown'а (например, 'data.unit_id')
            search_text: Не используется, оставлен для совместимости
            field_name: Название поля для логов
        """
        field_display = field_name or ng_model
        
        try:
            # Находим dropdown по ng-model
            dropdown_locator = self.page.locator(f'.ui.dropdown[ng-model="{ng_model}"]').first
            
            # Проверяем существование
            if dropdown_locator.count() == 0:
                print(f"  ⚠ {field_display} не заполнен: Dropdown не найден")
                return False
            
            # Прокручиваем только если элемент не виден
            if not dropdown_locator.is_visible():
                dropdown_locator.scroll_into_view_if_needed(timeout=3000)
                self.wait_for_load(100)
            
            # Открываем dropdown кликом
            dropdown_locator.click(timeout=3000)
            self.wait_for_load(300)  # Пауза для открытия меню
            
            # Находим меню и первый доступный элемент
            menu = dropdown_locator.locator('.menu').first
            items = menu.locator('.item:not(.disabled)')
            
            # Ждем появления элементов
            try:
                items.first.wait_for(state='visible', timeout=3000)
            except:
                pass  # Продолжаем даже если не дождались
            
            items_count = items.count()
            if items_count == 0:
                print(f"  ⚠ {field_display} не заполнен: В меню нет доступных пунктов")
                return False
            
            # Выбираем первый элемент
            first_item = items.first
            try:
                # Получаем текст перед кликом
                item_text = first_item.text_content(timeout=1000).strip()
                first_item.click(timeout=3000)
                print(f"  ✓ {field_display}: {item_text}")
                self.wait_for_load(200)  # Минимальная пауза
                return True
            except Exception as e:
                # Если обычный клик не сработал, пробуем force
                try:
                    first_item.click(force=True, timeout=3000)
                    print(f"  ✓ {field_display}: выбран первый элемент")
                    self.wait_for_load(200)
                    return True
                except:
                    print(f"  ⚠ {field_display} не заполнен: Не удалось кликнуть на элемент: {e}")
                    return False
                
        except Exception as e:
            print(f"  ⚠ {field_display} не заполнен: {e}")
            return False
    
    def _select_multiple_dropdown_by_ng_model(self, ng_model: str, search_text: str = None, field_name: str = None):
        """
        Оптимизированный метод для заполнения dropdown'а с множественным выбором через Playwright API
        Открывает меню и выбирает первый доступный элемент
        
        Args:
            ng_model: Значение ng-model атрибута dropdown'а (например, 'data.categories')
            search_text: Не используется, оставлен для совместимости
            field_name: Название поля для логов
        """
        field_display = field_name or ng_model
        
        try:
            # Находим dropdown по ng-model
            dropdown_locator = self.page.locator(f'.ui.dropdown[ng-model="{ng_model}"]').first
            
            # Проверяем существование
            if dropdown_locator.count() == 0:
                print(f"  ⚠ {field_display} не заполнен: Dropdown не найден")
                return False
            
            # Прокручиваем только если элемент не виден
            if not dropdown_locator.is_visible():
                dropdown_locator.scroll_into_view_if_needed(timeout=3000)
                self.wait_for_load(100)
            
            # Открываем dropdown кликом
            dropdown_locator.click(timeout=3000)
            self.wait_for_load(300)  # Пауза для открытия меню
            
            # Находим меню и первый доступный элемент
            menu = dropdown_locator.locator('.menu').first
            items = menu.locator('.item:not(.disabled)')
            
            # Ждем появления элементов
            try:
                items.first.wait_for(state='visible', timeout=3000)
            except:
                pass  # Продолжаем даже если не дождались
            
            items_count = items.count()
            if items_count == 0:
                print(f"  ⚠ {field_display} не заполнен: В меню нет доступных пунктов")
                return False
            
            # Выбираем первый элемент (для multiple selection может потребоваться force)
            first_item = items.first
            try:
                # Получаем текст перед кликом
                item_text = first_item.text_content(timeout=1000).strip()
                first_item.click(timeout=3000)
                print(f"  ✓ {field_display}: {item_text}")
                self.wait_for_load(200)  # Минимальная пауза
                return True
            except Exception as e:
                # Если обычный клик не сработал, пробуем force (важно для multiple selection)
                try:
                    first_item.click(force=True, timeout=3000)
                    print(f"  ✓ {field_display}: выбран первый элемент")
                    self.wait_for_load(200)
                    return True
                except:
                    print(f"  ⚠ {field_display} не заполнен: Не удалось кликнуть на элемент: {e}")
                    return False
                
        except Exception as e:
            print(f"  ⚠ {field_display} не заполнен: {e}")
            return False
    
    def _fill_dropdowns_in_order(self, category: str = None, marking_type: str = None,
                                 country: str = None, tax_system: str = None, 
                                 taxes: list = None, supplier: str = None):
        """
        Приватный метод для заполнения всех dropdown'ов формы по порядку сверху вниз
        Заполнение происходит последовательно для предотвращения скачков модального окна
        
        Args:
            category: Категория (multiple selection) - сверху
            marking_type: Тип маркировки - сверху
            country: Страна - в середине
            tax_system: Система налогообложения - в середине
            taxes: Список налогов (multiple selection) - внизу
            supplier: Поставщик - внизу
        """
        # Заполняем все dropdown'ы последовательно с минимальными паузами
        # 1. Категория (multiple selection) - обычно вверху формы
        if category:
            self._select_multiple_dropdown_by_ng_model(self.DROPDOWN_CATEGORY, category, "Категория")
        
        # 2. Тип маркировки - обычно вверху формы
        if marking_type:
            self._select_dropdown_by_ng_model(self.DROPDOWN_MARKING_TYPE, marking_type, "Тип маркировки")
        
        # 3. Страна - в середине формы
        if country:
            self._select_dropdown_by_ng_model(self.DROPDOWN_COUNTRY, country, "Страна")
        
        # 4. Система налогообложения - в середине формы
        if tax_system:
            self._select_dropdown_by_ng_model(self.DROPDOWN_TAX_SYSTEM, tax_system, "Система налогообложения")
        
        # 5. Налоги (multiple selection) - можно выбрать несколько, обычно внизу
        if taxes:
            for tax in taxes:
                if tax:  # Проверяем, что налог не пустой
                    self._select_multiple_dropdown_by_ng_model(self.DROPDOWN_TAXES, tax, "Налог")
        
        # 6. Поставщик - обычно внизу формы
        if supplier:
            self._select_dropdown_by_ng_model(self.DROPDOWN_SUPPLIER, supplier, "Поставщик")
    
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
    
    def click_product_row(self, product_name: str):
        """
        Клик по ссылке товара в списке для открытия карточки
        
        Args:
            product_name: Название товара
        """
        result = self.page.evaluate(f"""
            (name) => {{
                // Ищем ссылку с названием товара
                const links = document.querySelectorAll('a');
                for (let link of links) {{
                    if (link.textContent.includes(name) && link.href.includes('/card/catalog/get/')) {{
                        link.click();
                        return true;
                    }}
                }}
                return false;
            }}
        """, product_name)
        
        if result:
            # Ждем загрузки модального окна просмотра - URL изменяется на .../m/get/<id>
            self.page.wait_for_url("**/m/get/**", timeout=10000)
            self.wait_for_load(2000)
            print(f"  ✓ Открыто окно просмотра товара '{product_name}'")
            return True
        else:
            raise Exception(f"Ссылка на товар '{product_name}' не найдена в списке")
    
    def click_edit_button(self):
        """
        Нажать кнопку 'Редактировать' в модальном окне просмотра товара
        """
        try:
            # Ищем элемент с cursor:pointer и текстом "Редактировать"
            result = self.page.evaluate("""
                () => {
                    const elements = Array.from(document.querySelectorAll('*'));
                    for (let el of elements) {
                        const style = window.getComputedStyle(el);
                        const text = el.textContent.trim();
                        
                        // Проверяем, что это кликабельный элемент с текстом "Редактировать"
                        if (style.cursor === 'pointer' && text === 'Редактировать' && el.children.length === 0) {
                            el.click();
                            return true;
                        }
                    }
                    return false;
                }
            """)
            
            if result:
                self.wait_for_load(2000)
                print("  ✓ Кнопка 'Редактировать' нажата")
            else:
                raise Exception("Кнопка 'Редактировать' не найдена")
        except Exception as e:
            raise Exception(f"Не удалось нажать 'Редактировать': {e}")
    
    def update_product_fields(self, name: str = None, price: int = None):
        """
        Обновление полей товара в форме редактирования
        
        Args:
            name: Новое название
            price: Новая цена
        """
        # Обновляем название
        if name:
            modal_inputs = self.page.locator(self.MODAL_NAME_INPUT)
            if modal_inputs.count() > 1:
                name_input = modal_inputs.nth(1)
                name_input.fill("")  # Очищаем
                name_input.fill(name)
                print(f"  ✓ Новое название: {name}")
        
        # Обновляем цену
        if price:
            # Скроллим модальное окно вниз
            self.page.evaluate("""
                () => {
                    const modal = document.querySelector('.cs.sidebar, [ui-view="modal"]');
                    if (modal) modal.scrollTop = modal.scrollHeight;
                }
            """)
            self.wait_for_load(500)
            
            price_input = self.page.locator(self.MODAL_PRICE_SALE_INPUT).first
            if price_input.count() > 0:
                price_input.scroll_into_view_if_needed()
                price_input.fill(str(price))
                print(f"  ✓ Новая цена: {price}")
    
    def edit_product(self, product_name: str, **kwargs):
        """
        Редактирование товара
        
        Args:
            product_name: Название товара для редактирования
            **kwargs: Поля для обновления (name, price)
        """
        # Кликаем по строке товара
        self.click_product_row(product_name)
        
        # Нажимаем "Редактировать"
        self.click_edit_button()
        
        # Обновляем поля
        self.update_product_fields(**kwargs)
        
        # Сохраняем
        self.click_save()
        
        print(f"  ✓ Товар '{product_name}' отредактирован")
    
    def select_product_checkbox(self, product_name: str):
        """
        Выбрать чекбокс рядом с товаром
        
        Args:
            product_name: Название товара
        """
        result = self.page.evaluate(f"""
            (name) => {{
                const cells = Array.from(document.querySelectorAll('td, .item'));
                for (let cell of cells) {{
                    if (cell.innerText.includes(name)) {{
                        const row = cell.closest('tr, .row, .item');
                        if (row) {{
                            // Ищем checkbox в этой строке
                            const checkbox = row.querySelector('input[type="checkbox"], .checkbox');
                            if (checkbox) {{
                                checkbox.click();
                                return true;
                            }}
                        }}
                    }}
                }}
                return false;
            }}
        """, product_name)
        
        if result:
            self.wait_for_load(500)
            print(f"  ✓ Чекбокс товара '{product_name}' выбран")
        else:
            raise Exception(f"Чекбокс товара '{product_name}' не найден")
    
    def click_actions_dropdown(self):
        """
        Нажать на dropdown 'Действия над товаром'
        """
        try:
            # Ищем dropdown через JavaScript - это может быть кнопка или div с текстом "Действия"
            result = self.page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('*');
                    for (let el of elements) {
                        const text = el.innerText;
                        // Ищем элемент с текстом содержащим "Действия" и курсором pointer
                        if (text && text.includes('Действия') && text.length < 100) {
                            const style = window.getComputedStyle(el);
                            if (style.cursor === 'pointer' || el.tagName === 'BUTTON' || el.getAttribute('ng-click')) {
                                el.click();
                                return true;
                            }
                        }
                    }
                    return false;
                }
            """)
            
            if result:
                self.wait_for_load(1500)  # Даем время dropdown'у открыться
                print("  ✓ Dropdown 'Действия' открыт")
            else:
                raise Exception("Dropdown 'Действия' не найден")
        except Exception as e:
            raise Exception(f"Не удалось открыть dropdown 'Действия': {e}")
    
    def click_delete_in_actions(self):
        """
        Нажать 'Удалить' в dropdown действий
        """
        try:
            # Ищем элемент с ng-click="removeSelectedProducts()" через JavaScript
            result = self.page.evaluate("""
                () => {
                    // Ищем элемент с ng-click содержащим remove
                    const removeButton = document.querySelector('div[ng-click="removeSelectedProducts()"], [ng-click*="remove"]');
                    if (removeButton) {
                        removeButton.click();
                        return {success: true, method: 'ng-click'};
                    }
                    
                    // Альтернатива - ищем в видимых элементах dropdown
                    const items = Array.from(document.querySelectorAll('.item, .menu .item, div[permission*="delete"]'));
                    for (let item of items) {
                        const text = item.innerText.trim().toLowerCase();
                        const isVisible = item.offsetParent !== null;
                        
                        if (text === 'удалить' && isVisible) {
                            item.click();
                            return {success: true, method: 'visible item'};
                        }
                    }
                    
                    return {success: false};
                }
            """)
            
            if result and result.get('success'):
                self.wait_for_load(1500)
                print(f"  ✓ Кнопка 'Удалить' нажата ({result.get('method', 'unknown')})")
            else:
                raise Exception("Кнопка 'Удалить' не найдена в меню")
        except Exception as e:
            raise Exception(f"Не удалось нажать 'Удалить': {e}")
    
    def confirm_delete(self):
        """
        Подтвердить удаление товара в модальном окне подтверждения
        """
        try:
            # Ждем появления модального окна подтверждения
            self.wait_for_load(2000)
            
            # Ищем кнопку "Да" в модальном окне
            result = self.page.evaluate("""
                () => {
                    // Ищем все элементы, которые могут быть кнопками
                    const elements = Array.from(document.querySelectorAll('button, div.button, a.button, .ui.button, div[ng-click], [ng-click]'));
                    
                    // Фильтруем только видимые
                    const visible = elements.filter(el => {
                        const style = window.getComputedStyle(el);
                        return style.display !== 'none' && el.offsetParent !== null;
                    });
                    
                    // Ищем кнопку с текстом "Да"
                    for (let el of visible) {
                        const text = el.textContent.trim().toLowerCase();
                        if (text === 'да') {
                            el.click();
                            return {success: true, text: el.textContent.trim(), class: el.className};
                        }
                    }
                    
                    // Если не нашли "Да", ищем кнопку OK с классом right
                    for (let el of visible) {
                        const classes = el.className.toLowerCase();
                        if (classes.includes('ok') && classes.includes('right')) {
                            el.click();
                            return {success: true, text: el.textContent.trim(), class: el.className};
                        }
                    }
                    
                    // Возвращаем список доступных кнопок для отладки
                    return {
                        success: false, 
                        available: visible.map(el => ({
                            text: el.textContent.trim().substring(0, 30),
                            tag: el.tagName,
                            class: el.className.substring(0, 50)
                        })).slice(0, 5)
                    };
                }
            """)
            
            if result and result.get('success'):
                self.wait_for_load(2000)
                print(f"  ✓ Подтверждение 'Да' нажато (текст: '{result.get('text', '')}')")
            else:
                available = result.get('available', []) if result else []
                buttons_info = '\n    '.join([f"{b.get('text', '')} [{b.get('tag', '')}] (class: {b.get('class', '')})" for b in available])
                raise Exception(f"Кнопка 'Да' не найдена. Доступные кнопки:\n    {buttons_info}")
        except Exception as e:
            raise Exception(f"Не удалось подтвердить удаление: {e}")
    
    def delete_product(self, product_name: str):
        """
        Удаление товара
        
        Args:
            product_name: Название товара для удаления
        
        Шаги:
            1. Выбрать чекбокс товара
            2. Открыть dropdown 'Действия'
            3. Нажать 'Удалить'
            4. Подтвердить удаление (нажать "Да")
        """
        # Выбираем чекбокс
        self.select_product_checkbox(product_name)
        
        # Открываем dropdown действий
        self.click_actions_dropdown()
        
        # Кликаем "Удалить" - откроется модальное окно подтверждения
        self.click_delete_in_actions()
        
        # Подтверждаем удаление
        self.confirm_delete()
        
        print(f"  ✓ Товар '{product_name}' удален")

