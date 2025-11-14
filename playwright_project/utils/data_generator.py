"""
Генератор тестовых данных
"""

import random
import string
from datetime import datetime


class TestDataGenerator:
    """Класс для генерации тестовых данных"""
    
    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """Генерация случайной строки"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def generate_product_name() -> str:
        """Генерация названия товара"""
        prefixes = ["Тестовый", "Авто", "QA"]
        items = ["Товар", "Продукт", "Изделие", "Артикул"]
        timestamp = datetime.now().strftime("%H%M%S")
        return f"{random.choice(prefixes)} {random.choice(items)} {timestamp}"
    
    @staticmethod
    def generate_barcode() -> str:
        """Генерация штрих-кода (13 цифр)"""
        return ''.join([str(random.randint(0, 9)) for _ in range(13)])
    
    @staticmethod
    def generate_article() -> str:
        """Генерация артикула"""
        return f"ART-{random.randint(100, 999)}-{random.randint(100, 999)}"
    
    @staticmethod
    def generate_price() -> int:
        """Генерация цены"""
        return random.randint(100, 50000)
    
    @staticmethod
    def generate_product_data(full: bool = True) -> dict:
        """
        Генерация полного набора данных для товара
        
        Args:
            full: Если True, генерирует все возможные поля
        
        Returns:
            dict: Словарь с данными товара
        """
        base_data = {
            "name": TestDataGenerator.generate_product_name(),
            "barcode": TestDataGenerator.generate_barcode(),
            "article": TestDataGenerator.generate_article(),
            "price": TestDataGenerator.generate_price(),
            "description": f"Автоматически сгенерированное описание для тестового товара {datetime.now()}"
        }
        
        if full:
            base_data.update({
                "unit": random.choice(["шт", "кг", "л", "м", "упак"]),
                "category": random.choice(["Электроника", "Продукты", "Одежда", "Товары для дома"]),
                "country": random.choice(["Россия", "Китай", "США", "Германия"]),
                "purchase_price": random.randint(50, 500),
                "markup": random.randint(10, 100),
                "weight": round(random.uniform(0.1, 50.0), 2),
                "height": round(random.uniform(1, 100), 1),
                "width": round(random.uniform(1, 100), 1),
                "depth": round(random.uniform(1, 100), 1),
                "min_stock": random.randint(1, 10),
                "tax_code": str(random.randint(1000, 9999)),
                "supplier": random.choice(["Тестовщик", "Поставщик", "Поставщик номер десят"]),
                "marking_type": random.choice(["Без маркировки", "Обувь", "Изделия из меха"]),
                "tax_system": random.choice(["ЕСХН", "ОСНО", "ПСН", "УСН Доход"]),
                "taxes": [random.choice(["Tax 1", "Tax", "Test"])]  # Список из одного налога
            })
        
        return base_data
    
    @staticmethod
    def generate_email() -> str:
        """Генерация email"""
        return f"test.{TestDataGenerator.generate_random_string(8)}@example.com"
    
    @staticmethod
    def generate_phone() -> str:
        """Генерация телефона"""
        return f"+7{random.randint(9000000000, 9999999999)}"
    
    @staticmethod
    def generate_client_data() -> dict:
        """Генерация данных клиента"""
        return {
            "name": f"Тест Клиент {random.randint(1000, 9999)}",
            "phone": TestDataGenerator.generate_phone(),
            "email": TestDataGenerator.generate_email()
        }
    
    @staticmethod
    def generate_supplier_data() -> dict:
        """Генерация данных поставщика"""
        return {
            "name": f"Тестовый Поставщик {random.randint(1000, 9999)}",
            "inn": ''.join([str(random.randint(0, 9)) for _ in range(10)]),
            "phone": TestDataGenerator.generate_phone()
        }

