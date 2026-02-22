"""
Модуль SMS-верификации
Виртуальные номера для регистрации
"""

import random
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class SMSGateway:
    """
    Управление виртуальными номерами
    """
    
    def __init__(self):
        self.providers = {
            'smspva': {'api': 'https://smspva.com', 'countries': 20},
            '5sim': {'api': 'https://5sim.net', 'countries': 30},
            'smspool': {'api': 'https://smspool.net', 'countries': 50},
            'textnow': {'free': True, 'us_only': True}
        }
        
        self.active_numbers = {}
        self.verification_history = []
    
    def get_number(self, country: str = 'US', service: str = 'any') -> Dict:
        """
        Получение временного номера
        """
        number_id = self._generate_id()
        
        number = {
            'id': number_id,
            'country': country,
            'number': self._generate_phone_number(country),
            'service': service,
            'expires': (datetime.now() + timedelta(hours=24)).isoformat(),
            'status': 'active',
            'provider': random.choice(list(self.providers.keys())),
            'cost': self._calculate_cost(country, service)
        }
        
        self.active_numbers[number_id] = number
        return number
    
    def _generate_phone_number(self, country: str) -> str:
        """Генерация номера телефона"""
        codes = {
            'US': '+1',
            'RU': '+7',
            'GB': '+44',
            'DE': '+49',
            'FR': '+33'
        }
        
        country_code = codes.get(country, '+1')
        
        # Генерация остальной части номера
        if country == 'US':
            number = f"{country_code}{random.randint(200, 999)}{random.randint(200, 999)}{random.randint(1000, 9999)}"
        else:
            number = f"{country_code}{random.randint(100000000, 999999999)}"
        
        return number
    
    def _calculate_cost(self, country: str, service: str) -> float:
        """Расчёт стоимости номера"""
        base_costs = {
            'US': 0.50,
            'GB': 0.75,
            'RU': 0.30,
            'DE': 0.80,
            'FR': 0.80
        }
        
        service_multipliers = {
            'telegram': 2.0,
            'whatsapp': 1.5,
            'facebook': 1.2,
            'any': 1.0
        }
        
        return base_costs.get(country, 0.50) * service_multipliers.get(service, 1.0)
    
    def wait_for_sms(self, number_id: str, timeout: int = 120) -> Optional[str]:
        """
        Ожидание SMS-кода
        """
        if number_id not in active_numbers:
            return None
        
        number = self.active_numbers[number_id]
        start = time.time()
        
        while time.time() - start < timeout:
            # Здесь будет реальный запрос к API провайдера
            code = self._check_sms(number)
            if code:
                self.verification_history.append({
                    'number_id': number_id,
                    'code': code,
                    'time': datetime.now().isoformat(),
                    'success': True
                })
                return code
            
            time.sleep(5)
        
        self.verification_history.append({
            'number_id': number_id,
            'timeout': True,
            'time': datetime.now().isoformat(),
            'success': False
        })
        
        return None
    
    def _check_sms(self, number: Dict) -> Optional[str]:
        """Проверка SMS (заглушка)"""
        # В реальности здесь будет API запрос
        if random.random() < 0.3:  # 30% шанс получить код
            return str(random.randint(100000, 999999))
        return None
    
    def verify_code(self, number_id: str, code: str) -> bool:
        """
        Проверка введённого кода
        """
        for entry in self.verification_history:
            if entry.get('number_id') == number_id and entry.get('code') == code:
                return True
        return False
    
    def release_number(self, number_id: str) -> bool:
        """
        Освобождение номера
        """
        if number_id in self.active_numbers:
            del self.active_numbers[number_id]
            return True
        return False
    
    def _generate_id(self) -> str:
        """Генерация уникального ID"""
        import uuid
        return str(uuid.uuid4())[:12]
    
    def get_stats(self) -> Dict:
        """Статистика использования"""
        return {
            'active_numbers': len(self.active_numbers),
            'total_verifications': len(self.verification_history),
            'success_rate': len([v for v in self.verification_history if v.get('success')]) / max(len(self.verification_history), 1) * 100
        }


# Тестовый запуск
if __name__ == "__main__":
    sms = SMSGateway()
    
    # Получаем номер
    number = sms.get_number('US', 'telegram')
    print(f" Номер получен: {number['number']}")
    print(f" Стоимость: ${number['cost']}")
    
    # Ждём SMS
    print(" Ожидание SMS...")
    code = sms.wait_for_sms(number['id'])
    
    if code:
        print(f" Код получен: {code}")
        # Проверяем код
        if sms.verify_code(number['id'], code):
            print(" Верификация успешна")
    
    # Статистика
    print(f"\n Статистика: {sms.get_stats()}")
