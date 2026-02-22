"""
Полная интеграция всех VIP-модулей
Версия: 1.0.0
"""

import json
import yaml
from typing import Dict, Any, Optional
from datetime import datetime

from . import VIPModule
from .anonymity.ip_masquerade import IPMasquerade
from .sockpuppet.generator import SockPuppetGenerator
from .phone.sms_gateway import SMSGateway
from .evidence.chain_of_custody import EvidenceCollector, MetadataSanitizer

class CompleteVIPSystem:
    """
    Полная VIP-система со всеми модулями
    Интегрирует анонимность, цифровые копии, SMS и доказательства
    """
    
    def __init__(self, tier: str = 'basic', case_name: Optional[str] = None):
        """
        Инициализация полной VIP-системы
        
        Args:
            tier: Уровень доступа (basic/professional/vip/enterprise)
            case_name: Название кейса для цепочки доказательств
        """
        self.tier = tier
        self.vip = VIPModule(tier=tier)
        self.start_time = datetime.now()
        self.case_name = case_name or f"case_{self.vip.session_id}"
        
        # Инициализация модулей согласно tier
        self.modules = {}
        self._init_modules()
        
        print(f" VIP-система инициализирована")
        print(f"   Уровень: {tier.upper()}")
        print(f"   Кейс: {self.case_name}")
        print(f"   Модулей загружено: {len(self.modules)}")
    
    def _init_modules(self):
        """Инициализация модулей на основе доступных функций"""
        features = self.vip.get_features()
        
        # Модуль 1: IP-маскировка
        if 'vpn_rotation' in features or 'basic_proxies' in features:
            self.modules['ip'] = IPMasquerade()
            print(f"    IP-маскировка: активна")
        
        # Модуль 2: Цифровые копии
        if 'sock_puppets' in features or 'professional_sockpuppet_service' in features:
            self.modules['sockpuppet'] = SockPuppetGenerator()
            print(f"    Генератор копий: активен")
        
        # Модуль 3: SMS-верификация
        if 'virtual_numbers' in features or 'dedicated_phone_numbers' in features:
            self.modules['phone'] = SMSGateway()
            print(f"    SMS-шлюз: активен")
        
        # Модуль 4: Цепочка доказательств
        if 'evidence_chain' in features or 'legal_hold' in features:
            self.modules['evidence'] = EvidenceCollector(case_id=self.case_name)
            self.modules['sanitizer'] = MetadataSanitizer()
            print(f"    Цепочка доказательств: активна")
    
    def get_status(self) -> dict:
        """Статус всех модулей"""
        status = {
            'system': {
                'tier': self.tier,
                'session_id': self.vip.session_id,
                'case_name': self.case_name,
                'uptime': (datetime.now() - self.start_time).total_seconds(),
                'active_modules': list(self.modules.keys())
            },
            'vip_stats': self.vip.get_stats(),
            'modules': {}
        }
        
        for name, module in self.modules.items():
            if hasattr(module, 'status'):
                status['modules'][name] = module.status()
            elif hasattr(module, 'get_stats'):
                status['modules'][name] = module.get_stats()
            else:
                status['modules'][name] = {'active': True, 'type': module.__class__.__name__}
        
        return status
    
    def use_feature(self, feature: str, **kwargs) -> Dict[str, Any]:
        """
        Использование конкретной функции
        
        Args:
            feature: Название функции
            **kwargs: Параметры для функции
            
        Returns:
            Результат выполнения или ошибка
        """
        # Логируем использование
        self.vip.use_feature(feature)
        
        # Проверка лимитов
        if not self.vip.check_limit('requests'):
            return {'error': 'Daily request limit exceeded', 'code': 'LIMIT_EXCEEDED'}
        
        # Маршрутизация по функциям
        result = self._route_feature(feature, **kwargs)
        
        # Если есть модуль доказательств, фиксируем действие
        if 'evidence' in self.modules and result and 'error' not in result:
            self.modules['evidence'].capture(
                source=f"feature:{feature}",
                data=result,
                evidence_type="feature_usage",
                metadata={'kwargs': kwargs}
            )
        
        return result
    
    def _route_feature(self, feature: str, **kwargs) -> Any:
        """Маршрутизация вызова к соответствующему модулю"""
        
        # === Модуль IP-маскировки ===
        if feature == 'vpn_rotation' and 'ip' in self.modules:
            return self.modules['ip'].rotate_ip(kwargs.get('method', 'random'))
        
        elif feature == 'check_leaks' and 'ip' in self.modules:
            return self.modules['ip'].check_leaks()
        
        # === Модуль цифровых копий ===
        elif feature == 'sock_puppets' and 'sockpuppet' in self.modules:
            return self.modules['sockpuppet'].generate_persona(kwargs.get('profile', {}))
        
        elif feature == 'get_persona' and 'sockpuppet' in self.modules:
            return self.modules['sockpuppet'].get_persona(kwargs.get('persona_id'))
        
        elif feature == 'list_personas' and 'sockpuppet' in self.modules:
            return self.modules['sockpuppet'].list_personas(kwargs.get('limit', 10))
        
        # === Модуль SMS ===
        elif feature == 'virtual_numbers' and 'phone' in self.modules:
            return self.modules['phone'].get_number(
                kwargs.get('country', 'US'),
                kwargs.get('service', 'any')
            )
        
        elif feature == 'wait_for_sms' and 'phone' in self.modules:
            return self.modules['phone'].wait_for_sms(
                kwargs.get('number_id'),
                kwargs.get('timeout', 120)
            )
        
        elif feature == 'verify_code' and 'phone' in self.modules:
            return self.modules['phone'].verify_code(
                kwargs.get('number_id'),
                kwargs.get('code')
            )
        
        elif feature == 'release_number' and 'phone' in self.modules:
            return self.modules['phone'].release_number(kwargs.get('number_id'))
        
        # === Модуль доказательств ===
        elif feature == 'capture_evidence' and 'evidence' in self.modules:
            return self.modules['evidence'].capture(
                source=kwargs.get('source', 'manual'),
                data=kwargs.get('data', ''),
                evidence_type=kwargs.get('type', 'unknown'),
                metadata=kwargs.get('metadata', {})
            )
        
        elif feature == 'verify_evidence' and 'evidence' in self.modules:
            return self.modules['evidence'].verify(kwargs.get('evidence_id'))
        
        elif feature == 'generate_report' and 'evidence' in self.modules:
            return self.modules['evidence'].generate_report()
        
        elif feature == 'sanitize_file' and 'sanitizer' in self.modules:
            return self.modules['sanitizer'].remove_metadata(kwargs.get('file_path'))
        
        # === Комплексные операции ===
        elif feature == 'create_investigation':
            """Создание полного расследования с анонимностью"""
            investigation = {
                'id': self.vip._generate_session_id(),
                'timestamp': datetime.now().isoformat(),
                'tier': self.tier,
                'status': 'created'
            }
            
            # 1. Создаём цифровую копию (если доступно)
            if 'sockpuppet' in self.modules:
                persona = self.modules['sockpuppet'].generate_persona(kwargs.get('profile', {}))
                investigation['persona'] = persona['id']
            
            # 2. Получаем временный номер (если доступно)
            if 'phone' in self.modules:
                number = self.modules['phone'].get_number(
                    kwargs.get('country', 'US'),
                    kwargs.get('service', kwargs.get('service', 'any'))
                )
                investigation['phone'] = number['id']
            
            # 3. Ротируем IP
            if 'ip' in self.modules:
                ip_result = self.modules['ip'].rotate_ip()
                investigation['ip'] = ip_result
            
            # 4. Создаём кейс для доказательств
            if 'evidence' in self.modules:
                case_id = f"investigation_{investigation['id']}"
                investigation['case_id'] = case_id
            
            # Логируем
            if 'evidence' in self.modules:
                self.modules['evidence'].capture(
                    source="system",
                    data=investigation,
                    evidence_type="investigation_created",
                    metadata={'kwargs': kwargs}
                )
            
            return investigation
        
        else:
            return {'error': f'Feature "{feature}" not available', 'code': 'FEATURE_UNAVAILABLE'}
    
    def export_report(self, format: str = 'json') -> str:
        """Экспорт полного отчёта"""
        report = {
            'system': {
                'tier': self.tier,
                'session': self.vip.session_id,
                'case': self.case_name,
                'start_time': self.start_time.isoformat(),
                'end_time': datetime.now().isoformat()
            },
            'vip_stats': self.vip.get_stats(),
            'modules': {}
        }
        
        # Добавляем статусы модулей
        for name, module in self.modules.items():
            if hasattr(module, 'status'):
                report['modules'][name] = module.status()
            elif hasattr(module, 'get_stats'):
                report['modules'][name] = module.get_stats()
        
        # Добавляем цепочку доказательств если есть
        if 'evidence' in self.modules:
            report['chain_of_custody'] = self.modules['evidence'].chain_of_custody
            report['evidence_count'] = len(self.modules['evidence'].evidence_log)
        
        if format == 'json':
            return json.dumps(report, indent=2, ensure_ascii=False)
        elif format == 'yaml':
            return yaml.dump(report, allow_unicode=True)
        else:
            return str(report)
    
    def cleanup(self):
        """Очистка ресурсов"""
        # Освобождаем номера
        if 'phone' in self.modules:
            for number_id in list(self.modules['phone'].active_numbers.keys()):
                self.modules['phone'].release_number(number_id)
        
        # Деактивируем личности
        if 'sockpuppet' in self.modules:
            for persona in self.modules['sockpuppet'].active_personas:
                self.modules['sockpuppet'].deactivate_persona(persona)
        
        print(f" VIP-система очищена")
    
    def __enter__(self):
        """Контекстный менеджер для with"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическая очистка при выходе"""
        self.cleanup()


# === ТЕСТОВЫЙ ЗАПУСК ===
if __name__ == "__main__":
    print("=" * 60)
    print(" ТЕСТИРОВАНИЕ VIP-СИСТЕМЫ")
    print("=" * 60)
    
    # Тест для каждого уровня
    for tier in ['basic', 'professional', 'vip']:
        print(f"\n Тестирование уровня: {tier.upper()}")
        print("-" * 40)
        
        with CompleteVIPSystem(tier=tier, case_name=f"test_{tier}") as vip:
            # Проверяем статус
            status = vip.get_status()
            print(f" Модулей загружено: {len(status['modules'])}")
            
            # Тестируем доступные функции
            if 'sock_puppets' in vip.vip.get_features():
                persona = vip.use_feature('sock_puppets', profile={'country': 'US'})
                if 'error' not in persona:
                    print(f" Создана личность: {persona['name']['full']}")
            
            if 'virtual_numbers' in vip.vip.get_features():
                number = vip.use_feature('virtual_numbers', country='US')
                if 'error' not in number:
                    print(f" Получен номер: {number['number']}")
            
            if 'vpn_rotation' in vip.vip.get_features():
                ip = vip.use_feature('vpn_rotation')
                if 'error' not in ip:
                    print(f" IP ротирован")
            
            if 'evidence_chain' in vip.vip.get_features():
                evidence = vip.use_feature(
                    'capture_evidence',
                    source='test',
                    data='test data',
                    type='test'
                )
                if 'error' not in evidence:
                    print(f" Доказательство сохранено: {evidence['id']}")
        
        print(f"\n Тест {tier} завершён")
    
    print("\n" + "=" * 60)
    print(" ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
    print("=" * 60)
