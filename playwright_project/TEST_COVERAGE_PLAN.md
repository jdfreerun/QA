# План покрытия CloudShop автотестами

## Анализ системы CloudShop

### Основные разделы (из навигации)
1. **Главная** — `/`
2. **Товары и услуги** — `/card/catalog/list`
3. **Смены** — `/authenticated.card.regist`
4. **Кассы** — `/authenticated.card.regist`
5. **Движение товара** — `/card/journal`
6. **Движение денег** — `/card/money`
7. **Отчеты** — `/card/reports`
8. **Поставщики** — `/authenticated.card.suppli`
9. **Клиенты** — `/authenticated.card.client`
10. **Настройки** — `/authenticated.card.compan`

### Типы документов
- Продажа — `/card/docs/sell`
- Закупка — `/card/docs/purchase`
- Возврат продажи — `/card/docs/return-sell`
- Возврат закупки — `/card/docs/return-purchase`
- Инвентаризация — `/card/docs/changes-invento`
- Оприходование — `/card/docs/changes-in`
- Списание — `/card/docs/changes-out`
- Перемещение — `/card/docs/moving`

### Операции с деньгами
- Приход — `/card/pay/cash-parish`
- Расход — `/card/pay/cash-outflow`
- Перевод — `/card/pay/cash-transfer`

---

## План покрытия автотестами

### 1. Модуль: Авторизация и безопасность

#### 1.1 Позитивные сценарии
- ✅ **test_login_success** — успешная авторизация с корректными данными
- **test_login_remember_me** — авторизация с чекбоксом "Запомнить меня"
- **test_qr_code_login** — авторизация через QR-код
- **test_logout** — выход из системы

#### 1.2 Негативные сценарии
- **test_login_invalid_email** — авторизация с некорректным email
- **test_login_invalid_password** — авторизация с неверным паролем
- **test_login_empty_fields** — авторизация с пустыми полями
- **test_login_sql_injection** — проверка на SQL-инъекции
- **test_login_xss** — проверка на XSS-атаки
- **test_password_reset** — восстановление пароля

#### 1.3 Регистрация
- **test_registration_new_user** — регистрация нового пользователя
- **test_registration_duplicate_email** — регистрация с существующим email
- **test_registration_validation** — проверка валидации полей при регистрации

---

### 2. Модуль: Товары и услуги

#### 2.1 CRUD операции с товарами
- ✅ **test_create_product** — создание товара с обязательными полями
- **test_create_product_full** — создание товара со всеми полями
- **test_create_service** — создание услуги (без остатков)
- **test_create_bundle** — создание комплекта товаров
- **test_read_product** — просмотр карточки товара
- **test_update_product** — редактирование товара
- **test_delete_product** — удаление товара
- **test_restore_product** — восстановление удаленного товара

#### 2.2 Управление товарами
- **test_product_search** — поиск товара по названию
- **test_product_filter_by_category** — фильтрация по категориям
- **test_product_sort** — сортировка товаров (по цене, названию, артикулу)
- **test_product_bulk_operations** — массовые операции (удаление, изменение цен)
- **test_product_export** — экспорт товаров в Excel/CSV
- **test_product_import** — импорт товаров из файла
- **test_product_barcode_generation** — генерация штрих-кодов
- **test_product_ikpu_code** — поиск и присвоение кода ИКПУ

#### 2.3 Валидация товаров
- **test_product_required_fields** — проверка обязательных полей
- **test_product_unique_barcode** — уникальность штрих-кода
- **test_product_negative_price** — попытка установить отрицательную цену
- **test_product_special_characters** — обработка спецсимволов в названии

#### 2.4 Типы товаров
- **test_tobacco_product** — создание табачной продукции с маркировкой
- **test_alcohol_product** — создание алкогольной продукции с маркировкой

---

### 3. Модуль: Документы движения товаров

#### 3.1 Продажи
- **test_create_sale_document** — создание документа продажи
- **test_sale_with_discount** — продажа со скидкой
- **test_sale_multiple_items** — продажа нескольких товаров
- **test_sale_payment_methods** — различные способы оплаты (наличные, карта, смешанная)
- **test_sale_print_receipt** — печать чека
- **test_cancel_sale** — отмена продажи

#### 3.2 Возвраты
- **test_return_sale** — возврат товара по продаже
- **test_partial_return** — частичный возврат товара
- **test_return_refund** — возврат денег клиенту

#### 3.3 Закупки
- **test_create_purchase** — создание документа закупки
- **test_purchase_from_supplier** — закупка у поставщика
- **test_return_purchase** — возврат товара поставщику

#### 3.4 Перемещения и списания
- **test_product_movement** — перемещение товара между складами
- **test_product_writeoff** — списание товара
- **test_product_acceptance** — оприходование товара
- **test_inventory** — инвентаризация

---

### 4. Модуль: Кассовые операции

#### 4.1 Работа с кассой
- **test_open_shift** — открытие смены
- **test_close_shift** — закрытие смены с отчетом
- **test_cash_income** — внесение наличных в кассу
- **test_cash_expense** — изъятие наличных из кассы
- **test_cash_transfer** — перевод между кассами
- **test_shift_report** — отчет по смене

#### 4.2 Интерфейс кассира
- **test_cashier_interface** — проверка интерфейса кассира
- **test_fast_sale** — быстрая продажа через интерфейс кассира

---

### 5. Модуль: Справочники

#### 5.1 Клиенты
- **test_create_client** — создание клиента
- **test_update_client** — редактирование клиента
- **test_delete_client** — удаление клиента
- **test_client_search** — поиск клиента
- **test_client_loyalty_program** — программа лояльности
- **test_client_purchase_history** — история покупок клиента

#### 5.2 Поставщики
- **test_create_supplier** — создание поставщика
- **test_update_supplier** — редактирование поставщика
- **test_delete_supplier** — удаление поставщика
- **test_supplier_orders** — заказы у поставщика

---

### 6. Модуль: Отчеты и аналитика

#### 6.1 Финансовые отчеты
- **test_sales_report** — отчет по продажам
- **test_profit_report** — отчет по прибыли
- **test_revenue_report** — отчет по выручке
- **test_tax_report** — налоговый отчет

#### 6.2 Товарные отчеты
- **test_stock_report** — отчет по остаткам
- **test_product_turnover** — оборачиваемость товаров
- **test_abc_analysis** — ABC-анализ товаров
- **test_expiring_products** — товары с истекающим сроком годности

#### 6.3 Отчеты по клиентам
- **test_top_clients_report** — топ клиентов
- **test_client_debt_report** — задолженность клиентов

---

### 7. Модуль: Настройки

#### 7.1 Настройки компании
- **test_company_profile** — редактирование профиля компании
- **test_company_logo** — загрузка логотипа
- **test_fiscal_settings** — настройки фискализации

#### 7.2 Настройки пользователей
- **test_create_user** — создание пользователя
- **test_user_roles** — назначение ролей пользователям
- **test_user_permissions** — настройка прав доступа
- **test_user_delete** — удаление пользователя

#### 7.3 Настройки системы
- **test_payment_methods_settings** — настройка способов оплаты
- **test_tax_settings** — настройка налогов
- **test_warehouse_settings** — настройка складов
- **test_notification_settings** — настройка уведомлений

---

### 8. Модуль: Интеграции

#### 8.1 Онлайн-касса
- **test_online_cash_register** — подключение онлайн-кассы
- **test_receipt_sending** — отправка чеков по email/SMS

#### 8.2 Экспорт/Импорт
- **test_export_to_excel** — экспорт данных в Excel
- **test_import_from_excel** — импорт из Excel
- **test_1c_integration** — интеграция с 1С

#### 8.3 API
- **test_api_authentication** — API авторизация
- **test_api_get_products** — получение товаров через API
- **test_api_create_sale** — создание продажи через API

---

### 9. Модуль: UI/UX

#### 9.1 Адаптивность
- **test_mobile_responsive** — проверка мобильной версии
- **test_tablet_responsive** — проверка планшетной версии
- **test_desktop_responsive** — проверка десктопной версии

#### 9.2 Производительность
- **test_page_load_time** — время загрузки страниц
- **test_large_catalog_performance** — производительность с большим каталогом
- **test_concurrent_users** — работа при множественных пользователях

#### 9.3 Кроссбраузерность
- **test_chrome_compatibility** — работа в Chrome
- **test_firefox_compatibility** — работа в Firefox
- **test_safari_compatibility** — работа в Safari
- **test_edge_compatibility** — работа в Edge

---

### 10. Модуль: Граничные условия и стресс-тесты

#### 10.1 Граничные значения
- **test_max_product_name_length** — максимальная длина названия товара
- **test_max_products_in_document** — максимум товаров в документе
- **test_zero_quantity_handling** — обработка нулевых остатков
- **test_negative_stock** — работа с отрицательными остатками

#### 10.2 Стресс-тесты
- **test_1000_products_creation** — создание 1000 товаров
- **test_large_file_import** — импорт большого файла
- **test_simultaneous_sales** — одновременные продажи

---

## Приоритизация тестов

### P0 (Критические — блокеры)
- Авторизация
- Создание/редактирование товаров
- Создание документов продажи
- Работа с кассой
- Открытие/закрытие смен

### P1 (Высокий приоритет)
- Возвраты
- Закупки
- Перемещения
- Работа с клиентами
- Основные отчеты

### P2 (Средний приоритет)
- Импорт/экспорт
- Настройки
- Дополнительные отчеты
- Поставщики

### P3 (Низкий приоритет)
- UI/UX тесты
- Кроссбраузерность
- Граничные условия
- Интеграции

---

## Структура проекта автотестов

```
playwright_project/
├── tests/
│   ├── auth/
│   │   ├── test_login.py
│   │   ├── test_registration.py
│   │   └── test_password_reset.py
│   ├── products/
│   │   ├── test_product_crud.py
│   │   ├── test_product_search.py
│   │   ├── test_product_import_export.py
│   │   └── test_product_validation.py
│   ├── documents/
│   │   ├── test_sales.py
│   │   ├── test_returns.py
│   │   ├── test_purchases.py
│   │   └── test_movements.py
│   ├── cash/
│   │   ├── test_shifts.py
│   │   ├── test_cash_operations.py
│   │   └── test_cashier_interface.py
│   ├── directories/
│   │   ├── test_clients.py
│   │   └── test_suppliers.py
│   ├── reports/
│   │   ├── test_financial_reports.py
│   │   ├── test_inventory_reports.py
│   │   └── test_client_reports.py
│   ├── settings/
│   │   ├── test_company_settings.py
│   │   ├── test_user_management.py
│   │   └── test_system_settings.py
│   ├── integrations/
│   │   ├── test_api.py
│   │   └── test_import_export.py
│   └── ui/
│       ├── test_responsive.py
│       └── test_cross_browser.py
├── fixtures/
│   ├── auth_fixtures.py
│   ├── product_fixtures.py
│   └── document_fixtures.py
├── pages/ (Page Object Model)
│   ├── login_page.py
│   ├── products_page.py
│   ├── sales_page.py
│   └── ...
├── utils/
│   ├── helpers.py
│   ├── data_generator.py
│   └── api_client.py
├── data/
│   ├── test_products.json
│   └── test_users.json
├── config/
│   ├── config.py
│   └── environments.py
├── conftest.py
├── pytest.ini
└── requirements.txt
```

---

## Метрики покрытия

### Целевые показатели
- **Функциональное покрытие**: 85%+
- **Покрытие критического функционала (P0)**: 100%
- **Покрытие регрессионными тестами**: 70%+
- **Автоматизация smoke-тестов**: 100%

### Текущее состояние
- ✅ Авторизация: 1/9 тестов (11%)
- ✅ Товары: 1/25 тестов (4%)
- Остальные модули: 0%

---

## План реализации (по спринтам)

### Спринт 1 (2 недели) — Основа и критический функционал
- Настройка инфраструктуры (fixtures, Page Objects)
- Завершение модуля авторизации (P0)
- CRUD товаров полностью (P0)
- Создание документа продажи (P0)

### Спринт 2 (2 недели) — Документооборот
- Возвраты (P1)
- Закупки (P1)
- Перемещения и списания (P1)
- Работа с кассой (P0)

### Спринт 3 (2 недели) — Справочники и отчеты
- Клиенты (P1)
- Поставщики (P2)
- Основные финансовые отчеты (P1)
- Товарные отчеты (P1)

### Спринт 4 (2 недели) — Настройки и интеграции
- Настройки компании и пользователей (P2)
- Импорт/экспорт (P2)
- API тесты (P2)

### Спринт 5 (1 неделя) — UI/UX и кроссбраузерность
- Адаптивность (P3)
- Кроссбраузерность (P3)
- Граничные условия (P3)

---

## Инструменты и технологии

### Основной стек
- **Playwright** — автоматизация UI
- **pytest** — фреймворк тестирования
- **Python 3.9+** — язык программирования
- **Allure** — отчетность
- **Jenkins/GitLab CI** — CI/CD

### Вспомогательные инструменты
- **Faker** — генерация тестовых данных
- **requests** — API тестирование
- **pytest-xdist** — параллельный запуск
- **pytest-html** — HTML отчеты
- **python-dotenv** — управление конфигурацией

---

## CI/CD Pipeline

```yaml
stages:
  - lint
  - test_smoke
  - test_regression
  - test_full
  - report

smoke_tests:
  stage: test_smoke
  script:
    - pytest -m smoke --alluredir=allure-results
  when: always

regression_tests:
  stage: test_regression
  script:
    - pytest -m "P0 or P1" --alluredir=allure-results
  when: on_schedule

full_tests:
  stage: test_full
  script:
    - pytest --alluredir=allure-results
  when: manual
```

---

## Выводы и рекомендации

1. **Приоритет на P0 и P1** — критический функционал должен быть покрыт в первую очередь
2. **Page Object Model** — использовать для поддерживаемости
3. **Параллелизация** — запускать тесты параллельно для ускорения
4. **Изоляция тестов** — каждый тест должен быть независимым
5. **Fixtures** — переиспользовать setup/teardown логику
6. **Data-driven подход** — параметризация тестов для разных наборов данных
7. **Регрессионный набор** — выделить стабильные тесты для ежедневного прогона
8. **Мониторинг** — отслеживать flaky tests и время выполнения

---

**Общая оценка трудозатрат**: ~400-500 часов (10-12 недель при команде из 2 QA automation)

**Ожидаемый результат**: Полное покрытие критического функционала (P0-P1) и частичное покрытие дополнительного (P2-P3)

