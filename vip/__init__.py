"""
VIP-модуль для OSINT_deepseek
Обеспечивает анонимность, цифровые копии и защиту доказательств
Версия: 0.1.0
"""

import os
import yaml
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

class VIPModule:
    """
    Главный класс VIP-функциональности
    Интегрируется с основным ядром OSINT_deepseek
    """
    
    def __init__(self, tier: str = 'basic', config_path: Optional[str] = None):
        """
        Инициализация VIP-модуля
        """
        self.tier = tier
        self.start_time = datetime.now()
        self.session_id = self._generate_session_id()
        
        # Загружаем конфигурацию
        if config_path:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            # Ищем в стандартном месте
            config_file = Path(__file__).parent / 'config' / 'tiers.yaml'
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        
        self.tier_config = self.config['tiers'].get(tier, self.config['tiers']['basic'])
        
        # Статистика
        self.stats = {
            'session_id': self.session_id,
            'tier': tier,
            'started': self.start_time.isoformat(),
            'requests': 0,
            'data_used_mb': 0,
            'features_used': []
        }
        
        # Модули будут инициализироваться по мере использования
        self._modules = {}
        
        print(f" VIP модуль инициализирован для tier: {tier}")
        print(f" Доступные функции: {len(self.tier_config['features'])}")
    
    def _generate_session_id(self) -> str:
        """Генерация уникального ID сессии"""
        import uuid
        return str(uuid.uuid4())[:12]
    
    def get_features(self) -> List[str]:
        """Получение списка доступных функций"""
        return self.tier_config['features']
    
    def get_limits(self) -> dict:
        """Получение лимитов для текущего tier"""
        return self.tier_config['limits']
    
    def check_limit(self, resource: str) -> bool:
        """
        Проверка лимитов
        """
        limits = self.get_limits()
        
        if resource == 'requests':
            return self.stats['requests'] < limits.get('requests_per_day', 1000)
        elif resource == 'storage':
            return self.stats['data_used_mb'] < limits.get('data_storage_gb', 10) * 1024
        
        return True
    
    def use_feature(self, feature_name: str):
        """
        Логирование использования функции
        """
        if feature_name not in self.stats['features_used']:
            self.stats['features_used'].append(feature_name)
        
        self.stats['requests'] += 1
    
    def get_stats(self) -> dict:
        """Получение статистики сессии"""
        return {
            **self.stats,
            'active_time': (datetime.now() - self.start_time).total_seconds(),
            'limits_remaining': {
                'requests': self.get_limits().get('requests_per_day', 1000) - self.stats['requests'],
                'storage_gb': self.get_limits().get('data_storage_gb', 10) - (self.stats['data_used_mb'] / 1024)
            }
        }
    
    def export_stats(self, format: str = 'json') -> str:
        """
        Экспорт статистики
        """
        if format == 'json':
            return json.dumps(self.get_stats(), indent=2, ensure_ascii=False)
        elif format == 'yaml':
            return yaml.dump(self.get_stats(), allow_unicode=True)
        else:
            return str(self.get_stats())
    
    def __repr__(self) -> str:
        return f"<VIPModule tier={self.tier} session={self.session_id}>"


# Тестовый запуск
if __name__ == "__main__":
    # Тестируем разные уровни
    for tier in ['basic', 'professional', 'vip', 'enterprise']:
        vip = VIPModule(tier=tier)
        print(f"\n {tier.upper()}:")
        print(f"   Функции: {vip.get_features()[:3]}...")
        print(f"   Лимиты: {vip.get_limits()}")
        vip.use_feature('vpn_rotation')
        print(f"   Статистика: {vip.get_stats()['requests']} запросов")
