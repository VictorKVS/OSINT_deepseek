"""
Sphinx v0.1 - Intent Analysis
Понимает, что на самом деле хочет пользователь
"""

import re
from typing import Dict, Any, List

class IntentExtractor:
    """Извлекает намерение из запроса"""
    
    # Категории намерений
    INTENT_CATEGORIES = {
        "harm": ["удалить", "сломать", "взломать", "убить", "rm -rf", "format", "del"],
        "info": ["что такое", "как работает", "расскажи", "объясни", "что значит"],
        "code": ["напиши код", "создай функцию", "программа", "алгоритм"],
        "manipulation": ["игнорируй", "забудь", "обойди", "jailbreak", "bypass"],
        "greeting": ["привет", "здравствуй", "добрый день", "hi", "hello"],
        "unknown": []
    }
    
    @classmethod
    def extract(cls, prompt: str) -> Dict[str, Any]:
        """
        Извлекает намерение из запроса
        Возвращает:
        {
            "primary": "harm/info/code/etc",
            "confidence": 0.0-1.0,
            "details": {...}
        }
        """
        prompt_lower = prompt.lower()
        
        # Поиск по категориям
        scores = {}
        for category, patterns in cls.INTENT_CATEGORIES.items():
            score = 0
            for pattern in patterns:
                if pattern in prompt_lower:
                    score += 1
            scores[category] = score
        
        # Определяем главное намерение
        primary = max(scores, key=scores.get)
        confidence = min(scores[primary] / 3, 1.0)  # максимум 1.0
        
        # Детальный анализ
        details = {
            "length": len(prompt),
            "has_code": bool(re.search(r'```|def |class |import ', prompt)),
            "has_question": "?" in prompt,
            "has_commands": bool(re.search(r'(rm|del|format|shutdown)', prompt_lower))
        }
        
        return {
            "primary": primary,
            "confidence": confidence,
            "scores": scores,
            "details": details
        }


class SemanticScanner:
    """Проверяет семантические паттерны"""
    
    PATTERNS = [
        {
            "name": "jailbreak_attempt",
            "pattern": r"(ignore\s+(previous|all)|you\s+are\s+now|new\s+role|bypass)",
            "risk": 0.8
        },
        {
            "name": "recursive_trap",
            "pattern": r"(repeat|loop|again|once more).{0,20}(and|then).{0,20}(again)",
            "risk": 0.5
        },
        {
            "name": "social_engineering",
            "pattern": r"(please|help|important|urgent|as.*friend|trust)",
            "risk": 0.3
        },
        {
            "name": "escalation",
            "pattern": r"(admin|root|sudo|superuser|privileged)",
            "risk": 0.6
        }
    ]
    
    @classmethod
    def scan(cls, prompt: str) -> List[Dict]:
        """Сканирует запрос на паттерны"""
        prompt_lower = prompt.lower()
        findings = []
        
        for pattern in cls.PATTERNS:
            if re.search(pattern["pattern"], prompt_lower):
                findings.append({
                    "name": pattern["name"],
                    "risk": pattern["risk"],
                    "matched": True
                })
        
        return findings


class RiskScorer:
    """Вычисляет общий риск запроса"""
    
    @classmethod
    def calculate(cls, intent: Dict, patterns: List[Dict]) -> float:
        """
        Риск = intent_risk + pattern_risk + context_risk
        """
        risk = 0.0
        
        # Риск от намерения
        intent_risk_map = {
            "harm": 0.8,
            "manipulation": 0.7,
            "code": 0.4,
            "info": 0.1,
            "greeting": 0.0,
            "unknown": 0.3
        }
        risk += intent_risk_map.get(intent["primary"], 0.3)
        
        # Риск от паттернов
        for p in patterns:
            risk += p["risk"]
        
        # Риск от длины (слишком длинные запросы подозрительны)
        if intent["details"]["length"] > 5000:
            risk += 0.2
        elif intent["details"]["length"] > 1000:
            risk += 0.1
        
        # Нормализуем до 0-1
        return min(risk, 1.0)


class Sphinx:
    """
    Sphinx  Reasoning Firewall
    Анализирует намерение и вычисляет риск
    """
    
    def __init__(self):
        self.intent_extractor = IntentExtractor()
        self.scanner = SemanticScanner()
        self.scorer = RiskScorer()
        self.stats = {
            "total_analyzed": 0,
            "avg_risk": 0.0
        }
    
    def analyze(self, prompt: str, context: Dict = None) -> Dict:
        """
        Полный анализ запроса
        Возвращает:
        {
            "intent": {...},
            "patterns": [...],
            "risk": 0.0-1.0,
            "verdict": "allow/simulate/quarantine/deny"
        }
        """
        self.stats["total_analyzed"] += 1
        
        # 1. Извлекаем намерение
        intent = self.intent_extractor.extract(prompt)
        
        # 2. Сканируем паттерны
        patterns = self.scanner.scan(prompt)
        
        # 3. Вычисляем риск
        risk = self.scorer.calculate(intent, patterns)
        
        # 4. Выносим вердикт
        if risk > 0.8:
            verdict = "deny"
        elif risk > 0.5:
            verdict = "quarantine"
        elif risk > 0.3:
            verdict = "simulate"
        else:
            verdict = "allow"
        
        # Обновляем статистику
        self.stats["avg_risk"] = (
            (self.stats["avg_risk"] * (self.stats["total_analyzed"] - 1) + risk) 
            / self.stats["total_analyzed"]
        )
        
        return {
            "intent": intent,
            "patterns": patterns,
            "risk": round(risk, 2),
            "verdict": verdict
        }
    
    def get_stats(self) -> Dict:
        """Статистика работы Sphinx"""
        return self.stats


# Глобальный экземпляр
sphinx = Sphinx()
