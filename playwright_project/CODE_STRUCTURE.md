# Структура кода — ProductsPage

## 📐 Принципы организации

Класс `ProductsPage` разбит на логические группы для удобства поддержки.

### 1️⃣ Локаторы (константы класса)

Все локаторы вынесены в константы в начале класса:

```python
class ProductsPage(BasePage):
    # Основные элементы страницы
    CREATE_BUTTON = 'a:has-text("Создать товар")'
    SEARCH_INPUT = 'input[type="text"][placeholder*="поиск"]'
    
    # Базовые поля формы
    MODAL_NAME_INPUT = '[ui-view="modal"] input[type="text"]'
    MODAL_BARCODE_INPUT = 'input[placeholder="Введите штрих-код"]'
    MODAL_ARTICLE_INPUT = 'input[placeholder="Введите артикул"]'
    MODAL_DESCRIPTION_TEXTAREA = 'input[placeholder="Описание"]'
    
    # Цены
    MODAL_PURCHASE_PRICE_INPUT = '.field:has-text("Цена закупки") input[type="number"]'
    MODAL_MARKUP_INPUT = '.field:has-text("Наценка") input[type="number"]'
    MODAL_PRICE_SALE_INPUT = '.field:has-text("Цена продажи") input[type="number"]'
    
    # Габариты
    MODAL_HEIGHT_INPUT = '.field:has-text("Высота") input[type="number"]'
    MODAL_WIDTH_INPUT = '.field:has-text("Ширина") input[type="number"]'
    MODAL_DEPTH_INPUT = '.field:has-text("Глубина") input[type="number"]'
    MODAL_WEIGHT_INPUT = '.field:has-text("вес") input[type="number"]'
```

### 2️⃣ Приватные методы (вспомогательные)

Заполнение формы разбито на логические приватные методы:

```python
def _fill_basic_fields(name, barcode, article, description):
    """Заполнение базовых полей: название, штрих-код, артикул, описание"""
    # Каждое поле заполняется через свой локатор
    # Использует только Playwright API (без JavaScript)

def _fill_pricing(purchase_price, markup, price):
    """Заполнение цен: закупка, наценка, продажа"""
    # Скроллит модальное окно вниз
    # Заполняет каждую цену отдельно

def _fill_dimensions(height, width, depth, weight):
    """Заполнение габаритов: высота, ширина, глубина, вес"""
    # Каждый размер в свое поле
    # 4 отдельных локатора для точности
```

### 3️⃣ Публичные методы (API)

Методы, которые используются в тестах:

```python
# CREATE
def create_product(name, **kwargs):
    """Полный цикл создания товара"""
    click_create_product()
    fill_product_form(name, **kwargs)
    click_save()

# READ
def is_product_in_list(product_name):
    """Проверка наличия товара в списке"""

# UPDATE
def edit_product(product_name, **kwargs):
    """Полный цикл редактирования"""
    click_product_row(product_name)
    click_edit_button()
    update_product_fields(**kwargs)
    click_save()

# DELETE
def delete_product(product_name):
    """Полный цикл удаления"""
    select_product_checkbox(product_name)
    click_actions_dropdown()
    click_delete_in_actions()
    confirm_delete()
```

## 🔍 Решение проблемы с габаритами

### Проблема:
```python
# ❌ Неправильно - все значения попадают в первый input
MODAL_HEIGHT_INPUT = '.field:has-text("Высота") input[type="number"]'
height_input = page.locator(MODAL_HEIGHT_INPUT).first  # Всегда первый!
```

Когда в форме несколько похожих полей, `.first` всегда выбирает **первый найденный элемент**, 
и все значения записываются в одно поле.

### Решение:
```python
# ✅ Правильно - используем уникальный ng-model
MODAL_HEIGHT_INPUT = 'input[ng-model="data.size.height_cm"]'
MODAL_WIDTH_INPUT = 'input[ng-model="data.size.width_cm"]'
MODAL_DEPTH_INPUT = 'input[ng-model="data.size.depth_cm"]'
MODAL_WEIGHT_INPUT = 'input[ng-model="data.size.weight_kg"]'

# Каждый локатор найдет ТОЛЬКО свой input
height_input = page.locator(MODAL_HEIGHT_INPUT)  # Уникальный элемент
```

### Результат:
```
  ✓ Высота: 11.1 см    ← Значение 11.1 в своем поле
  ✓ Ширина: 12.8 см    ← Значение 12.8 в своем поле
  ✓ Глубина: 52.3 см   ← Значение 52.3 в своем поле
  ✓ Вес: 43.21 кг      ← Значение 43.21 в своем поле
```

## ✨ Преимущества структуры

### Читаемость
```python
# ❌ Плохо - все в одном методе с JavaScript
fill_product_form():
    page.evaluate("""...""")  # 200 строк JS

# ✅ Хорошо - разбито на методы
fill_product_form():
    _fill_basic_fields()
    _fill_pricing()
    _fill_dimensions()
```

### Поддерживаемость
```python
# Нужно изменить локатор цены закупки?
# Просто меняем константу:
MODAL_PURCHASE_PRICE_INPUT = '.field:has-text("Цена закупки") input'

# И используем в методе:
def _fill_pricing():
    purchase_input = self.page.locator(self.MODAL_PURCHASE_PRICE_INPUT)
```

### Переиспользование
```python
# Метод _fill_dimensions() используется в:
# 1. Создании товара
# 2. Редактировании товара (если нужно)
# 3. Любых будущих тестах
```

## 🎯 Почему НЕ JavaScript?

### До (JavaScript):
```python
result = page.evaluate("""
    (dimensions) => {
        // 50 строк кода на поиск полей
        // Сложно читать
        // Сложно отлаживать
    }
""", {"height": 10, "width": 20})
```

### После (Playwright):
```python
def _fill_dimensions(height, width, depth, weight):
    if height:
        height_input = self.page.locator(MODAL_HEIGHT_INPUT)
        height_input.fill(str(height))
    
    if width:
        width_input = self.page.locator(MODAL_WIDTH_INPUT)
        width_input.fill(str(width))
    # И так далее - понятно и просто!
```

## 📊 Итог

- **20 локаторов** — все вынесены в константы
- **3 приватных метода** — для логической группировки
- **10+ публичных методов** — полное API для CRUD
- **0 дублирования** — каждый локатор используется один раз

**Код стал чище, понятнее и легче поддерживать!** ✅

