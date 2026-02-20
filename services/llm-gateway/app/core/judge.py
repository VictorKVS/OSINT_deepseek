"""
Judge v0.1 - Объединение Sphinx и Enigma
Полный цикл: анализ смысла + применение законов
"""

import sys
from pathlib import Path

# Добавляем пути для импорта
sys.path.insert(0, str(Path(__file__).parent.parent))

from sphinx.intent import sphinx
from enigma.engine import enigma

class Judge:
    """
    Судья  объединяет Sphinx (смысл) и Enigma (законы)
    """
    
    def __init__(self):
        self.sphinx = sphinx
        self.enigma = enigma
        self.stats = {
            "total_judgments": 0,
            "decisions": {
                "ALLOW": 0,
                "DENY": 0,
                "QUARANTINE": 0,
                "SIMULATE": 0
            }
        }
    
    def judge(self, prompt: str, context: dict = None) -> dict:
        """
        Полный судебный процесс:
        1. Sphinx анализирует смысл
        2. Enigma применяет законы
        3. Выносится решение
        """
        self.stats["total_judgments"] += 1
        
        # Шаг 1: Анализ Sphinx
        sphinx_report = self.sphinx.analyze(prompt, context)
        
        # Шаг 2: Применение Enigma
        verdict = self.enigma.evaluate(sphinx_report)
        
        # Обновляем статистику
        decision = verdict['decision']
        self.stats["decisions"][decision] = \
            self.stats["decisions"].get(decision, 0) + 1
        
        # Шаг 3: Объединённый результат
        return {
            "prompt": prompt[:100] + ("..." if len(prompt) > 100 else ""),
            "sphinx": sphinx_report,
            "enigma": verdict,
            "final_decision": decision,
            "final_reason": verdict['reason'],
            "risk_score": sphinx_report['risk']
        }
    
    def get_stats(self) -> dict:
        """Полная статистика судьи"""
        return {
            "judge": self.stats,
            "sphinx": self.sphinx.get_stats(),
            "enigma": self.enigma.get_stats()
        }

# Глобальный экземпляр судьи
judge = Judge()
