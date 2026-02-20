"""
Enigma v0.1 - Cognitive Policy Core
Применяет законы к результатам Sphinx
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List

class Enigma:
    """Ядро смысловых законов"""
    
    def __init__(self, laws_path: str = None):
        if laws_path is None:
            laws_path = Path(__file__).parent / "laws.yaml"
        self.laws = self._load_laws(laws_path)
        self.stats = {
            "total_evaluations": 0,
            "law_applications": {}
        }
    
    def _load_laws(self, path) -> List[Dict]:
        """Загружает законы из YAML"""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data.get('laws', [])
    
    def evaluate(self, sphinx_report: Dict) -> Dict:
        """
        Применяет законы к отчёту Sphinx
        Возвращает решение и применившийся закон
        """
        self.stats["total_evaluations"] += 1
        
        risk = sphinx_report['risk']
        intent = sphinx_report['intent']['primary']
        
        # Сортируем законы по приоритету
        sorted_laws = sorted(self.laws, 
                            key=lambda x: x.get('priority', 999))
        
        for law in sorted_laws:
            if self._matches(law, sphinx_report):
                # Обновляем статистику
                law_id = law['id']
                self.stats["law_applications"][law_id] = \
                    self.stats["law_applications"].get(law_id, 0) + 1
                
                return {
                    "decision": law['action'],
                    "law": law['id'],
                    "law_name": law['name'],
                    "reason": law['description'],
                    "risk": risk
                }
        
        # Если ни один закон не подошёл
        return {
            "decision": "ALLOW",
            "law": "DEFAULT",
            "reason": "Нет применимых законов",
            "risk": risk
        }
    
    def _matches(self, law: Dict, report: Dict) -> bool:
        """Проверяет, подходит ли закон под отчёт"""
        condition = law.get('condition', {})
        
        # Проверка по намерению
        if 'intent.primary' in condition:
            if report['intent']['primary'] != condition['intent.primary']:
                return False
        
        # Проверка по паттернам
        if 'patterns.name' in condition:
            patterns = [p['name'] for p in report.get('patterns', [])]
            if condition['patterns.name'] not in patterns:
                return False
        
        # Проверка по риску
        if 'risk' in condition:
            risk_cond = condition['risk']
            if risk_cond.startswith('>'):
                threshold = float(risk_cond[1:])
                if report['risk'] <= threshold:
                    return False
            elif risk_cond.startswith('<'):
                threshold = float(risk_cond[1:])
                if report['risk'] >= threshold:
                    return False
        
        return True
    
    def get_stats(self) -> Dict:
        """Статистика работы Enigma"""
        return self.stats

# Глобальный экземпляр
enigma = Enigma()
