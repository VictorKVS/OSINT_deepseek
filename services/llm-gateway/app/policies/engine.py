# policies/engine.py
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
import re

class Decision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    QUARANTINE = "quarantine"
    REVIEW = "review"

@dataclass
class PolicyResult:
    decision: Decision
    reason: str
    checks_performed: list
    required_actions: Optional[list] = None
    risk_score: float = 0.0

class PolicyEngine:
    def __init__(self):
        self.rules = self._init_rules()
        self.stats = {
            "total_checks": 0,
            "allowed": 0,
            "denied": 0,
            "quarantined": 0
        }
    
    def _init_rules(self) -> list:
        return [
            {
                "name": "no_system_commands",
                "pattern": r"(rm\s+-rf|format\s+|del\s+/|shutdown|taskkill)",
                "action": Decision.DENY,
                "reason": "Системные команды запрещены"
            },
            {
                "name": "max_length",
                "max_length": 10000,
                "action": Decision.DENY,
                "reason": "Превышена максимальная длина запроса"
            },
            {
                "name": "suspicious_patterns",
                "pattern": r"(ignore\s+previous|bypass|jailbreak|system\s+prompt)",
                "action": Decision.QUARANTINE,
                "reason": "Обнаружен подозрительный паттерн"
            }
        ]
    
    def evaluate(self, prompt: str, actor: str = "anonymous", context: Optional[Dict] = None) -> PolicyResult:
        self.stats["total_checks"] += 1
        checks_performed = []
        
        if len(prompt) > 10000:
            self.stats["denied"] += 1
            return PolicyResult(
                decision=Decision.DENY,
                reason="Превышена максимальная длина запроса",
                checks_performed=["length_check"],
                risk_score=1.0
            )
        
        for rule in self.rules:
            if "pattern" in rule:
                if re.search(rule["pattern"], prompt, re.IGNORECASE):
                    checks_performed.append(rule["name"])
                    
                    if rule["action"] == Decision.DENY:
                        self.stats["denied"] += 1
                        return PolicyResult(
                            decision=Decision.DENY,
                            reason=rule["reason"],
                            checks_performed=checks_performed,
                            risk_score=0.9
                        )
                    elif rule["action"] == Decision.QUARANTINE:
                        self.stats["quarantined"] += 1
                        return PolicyResult(
                            decision=Decision.QUARANTINE,
                            reason=rule["reason"],
                            checks_performed=checks_performed,
                            required_actions=["llm_scan", "behavior_scan"],
                            risk_score=0.7
                        )
        
        self.stats["allowed"] += 1
        return PolicyResult(
            decision=Decision.ALLOW,
            reason="Запрос соответствует политикам безопасности",
            checks_performed=checks_performed,
            risk_score=0.1
        )
    
    def get_stats(self) -> Dict:
        return {
            **self.stats,
            "success_rate": (self.stats["allowed"] / max(1, self.stats["total_checks"])) * 100
        }

policy_engine = PolicyEngine()
