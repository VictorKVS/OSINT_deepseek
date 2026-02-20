#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Система отслеживания работы агентов
Показывает всё: что думает агент, какие инструменты вызывает, сколько времени тратит
"""

import time
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from colorama import init, Fore, Style

init()


@dataclass
class AgentThought:
    """Мысль агента (промежуточное рассуждение)"""
    id: str
    agent_name: str
    thought: str
    timestamp: str
    parent_id: Optional[str] = None


@dataclass
class AgentAction:
    """Действие агента (вызов инструмента)"""
    id: str
    agent_name: str
    tool_name: str
    tool_input: Dict[str, Any]
    timestamp: str
    thought_id: str


@dataclass
class AgentObservation:
    """Результат выполнения действия"""
    id: str
    agent_name: str
    observation: str
    timestamp: str
    action_id: str
    success: bool
    error: Optional[str] = None


@dataclass
class AgentResponse:
    """Финальный ответ агента"""
    id: str
    agent_name: str
    response: str
    timestamp: str
    thought_ids: List[str] = field(default_factory=list)
    action_ids: List[str] = field(default_factory=list)


@dataclass
class AgentTrace:
    """Полный трейс выполнения агента"""
    trace_id: str
    agent_name: str
    user_query: str
    start_time: str
    end_time: Optional[str] = None
    duration: Optional[float] = None
    thoughts: List[AgentThought] = field(default_factory=list)
    actions: List[AgentAction] = field(default_factory=list)
    observations: List[AgentObservation] = field(default_factory=list)
    final_response: Optional[AgentResponse] = None
    success: bool = True
    error: Optional[str] = None


class AgentTracker:
    """Прозрачный трекер работы агентов"""
    
    def __init__(self, log_dir: str = "logs/agents"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)
        
        # Активные трейсы
        self.active_traces: Dict[str, AgentTrace] = {}
        
        # История
        self.history_file = self.log_dir / "agent_history.json"
        self.history = self._load_history()
        
        # Счётчики
        self.total_traces = len(self.history)
        self.total_thoughts = 0
        self.total_actions = 0
        
        # Включить/выключить детальное логирование
        self.verbose = True
    
    def _load_history(self) -> List[Dict]:
        """Загружает историю трейсов"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Сохраняет историю"""
        # Оставляем последние 1000 трейсов
        recent = self.history[-1000:]
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(recent, f, indent=2, ensure_ascii=False)
    
    def start_trace(self, agent_name: str, user_query: str) -> str:
        """Начинает отслеживание работы агента"""
        trace_id = str(uuid.uuid4())[:8]
        
        trace = AgentTrace(
            trace_id=trace_id,
            agent_name=agent_name,
            user_query=user_query,
            start_time=datetime.now().isoformat()
        )
        
        self.active_traces[trace_id] = trace
        
        if self.verbose:
            print(f"\n{Fore.CYAN} НОВЫЙ ТРЕЙС [{trace_id}]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   Агент: {agent_name}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   Запрос: {user_query}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{''*60}{Style.RESET_ALL}")
        
        return trace_id
    
    def add_thought(self, trace_id: str, agent_name: str, thought: str, parent_id: Optional[str] = None) -> str:
        """Добавляет мысль агента"""
        trace = self.active_traces.get(trace_id)
        if not trace:
            return ""
        
        thought_id = f"thought_{len(trace.thoughts) + 1}"
        
        t = AgentThought(
            id=thought_id,
            agent_name=agent_name,
            thought=thought,
            timestamp=datetime.now().isoformat(),
            parent_id=parent_id
        )
        
        trace.thoughts.append(t)
        self.total_thoughts += 1
        
        if self.verbose:
            print(f"\n{Fore.YELLOW} МЫСЛЬ [{thought_id}]:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   {thought}{Style.RESET_ALL}")
        
        return thought_id
    
    def add_action(self, trace_id: str, agent_name: str, tool_name: str, tool_input: Dict[str, Any], thought_id: str) -> str:
        """Добавляет действие агента"""
        trace = self.active_traces.get(trace_id)
        if not trace:
            return ""
        
        action_id = f"action_{len(trace.actions) + 1}"
        
        action = AgentAction(
            id=action_id,
            agent_name=agent_name,
            tool_name=tool_name,
            tool_input=tool_input,
            timestamp=datetime.now().isoformat(),
            thought_id=thought_id
        )
        
        trace.actions.append(action)
        self.total_actions += 1
        
        if self.verbose:
            print(f"\n{Fore.MAGENTA} ДЕЙСТВИЕ [{action_id}]:{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}   Инструмент: {tool_name}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}   Входные данные: {json.dumps(tool_input, ensure_ascii=False)}{Style.RESET_ALL}")
        
        return action_id
    
    def add_observation(self, trace_id: str, agent_name: str, observation: str, action_id: str, success: bool = True, error: str = None) -> str:
        """Добавляет результат выполнения действия"""
        trace = self.active_traces.get(trace_id)
        if not trace:
            return ""
        
        obs_id = f"obs_{len(trace.observations) + 1}"
        
        obs = AgentObservation(
            id=obs_id,
            agent_name=agent_name,
            observation=observation,
            timestamp=datetime.now().isoformat(),
            action_id=action_id,
            success=success,
            error=error
        )
        
        trace.observations.append(obs)
        
        if self.verbose:
            if success:
                print(f"\n{Fore.GREEN} РЕЗУЛЬТАТ [{obs_id}]:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}   {observation[:200]}{'...' if len(observation) > 200 else ''}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED} ОШИБКА [{obs_id}]:{Style.RESET_ALL}")
                print(f"{Fore.RED}   {error}{Style.RESET_ALL}")
        
        return obs_id
    
    def end_trace(self, trace_id: str, final_response: str = None, success: bool = True, error: str = None) -> AgentTrace:
        """Завершает отслеживание"""
        trace = self.active_traces.get(trace_id)
        if not trace:
            return None
        
        trace.end_time = datetime.now().isoformat()
        trace.duration = (datetime.fromisoformat(trace.end_time) - 
                         datetime.fromisoformat(trace.start_time)).total_seconds()
        trace.success = success
        trace.error = error
        
        if final_response:
            response_id = f"response_{len(trace.thoughts)}"
            trace.final_response = AgentResponse(
                id=response_id,
                agent_name=trace.agent_name,
                response=final_response,
                timestamp=trace.end_time,
                thought_ids=[t.id for t in trace.thoughts],
                action_ids=[a.id for a in trace.actions]
            )
        
        # Сохраняем в историю
        trace_dict = asdict(trace)
        self.history.append(trace_dict)
        self._save_history()
        
        # Удаляем из активных
        del self.active_traces[trace_id]
        self.total_traces += 1
        
        if self.verbose:
            print(f"\n{Fore.CYAN}{''*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN} ТРЕЙС ЗАВЕРШЁН [{trace_id}]{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   Длительность: {trace.duration:.2f} сек{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   Мыслей: {len(trace.thoughts)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}   Действий: {len(trace.actions)}{Style.RESET_ALL}")
            if final_response:
                print(f"{Fore.CYAN}   Ответ: {final_response[:100]}{'...' if len(final_response) > 100 else ''}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        return trace
    
    def get_trace(self, trace_id: str) -> Optional[AgentTrace]:
        """Получает трейс по ID"""
        # Сначала ищем в активных
        if trace_id in self.active_traces:
            return self.active_traces[trace_id]
        
        # Потом в истории
        for t in self.history:
            if t['trace_id'] == trace_id:
                return t
        
        return None
    
    def get_recent_traces(self, n: int = 10) -> List[Dict]:
        """Возвращает последние n трейсов"""
        return self.history[-n:]
    
    def get_stats(self) -> Dict:
        """Возвращает статистику"""
        total = len(self.history)
        if total == 0:
            return {
                "total_traces": 0,
                "avg_duration": 0,
                "success_rate": 0,
                "avg_thoughts": 0,
                "avg_actions": 0
            }
        
        successful = sum(1 for t in self.history if t.get('success', False))
        avg_duration = sum(t.get('duration', 0) for t in self.history) / total
        avg_thoughts = sum(len(t.get('thoughts', [])) for t in self.history) / total
        avg_actions = sum(len(t.get('actions', [])) for t in self.history) / total
        
        return {
            "total_traces": total,
            "avg_duration": round(avg_duration, 2),
            "success_rate": round((successful / total) * 100, 1),
            "avg_thoughts": round(avg_thoughts, 1),
            "avg_actions": round(avg_actions, 1)
        }
    
    def export_trace(self, trace_id: str, format: str = 'json') -> str:
        """Экспортирует трейс в разных форматах"""
        trace = self.get_trace(trace_id)
        if not trace:
            return None
        
        if format == 'json':
            filename = self.log_dir / f"trace_{trace_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(trace, f, indent=2, ensure_ascii=False)
            return str(filename)
        
        elif format == 'md':
            filename = self.log_dir / f"trace_{trace_id}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Трейс агента: {trace['agent_name']}\n\n")
                f.write(f"**Запрос:** {trace['user_query']}\n\n")
                f.write(f"**Начало:** {trace['start_time']}\n")
                f.write(f"**Конец:** {trace['end_time']}\n")
                f.write(f"**Длительность:** {trace.get('duration', 0):.2f} сек\n")
                f.write(f"**Успех:** {'' if trace.get('success') else ''}\n\n")
                
                if trace.get('thoughts'):
                    f.write("## Мысли\n\n")
                    for t in trace['thoughts']:
                        f.write(f"### {t['id']}\n")
                        f.write(f"{t['thought']}\n\n")
                
                if trace.get('actions'):
                    f.write("## Действия\n\n")
                    for a in trace['actions']:
                        f.write(f"### {a['id']}\n")
                        f.write(f"**Инструмент:** {a['tool_name']}\n")
                        f.write(f"**Вход:** `{json.dumps(a['tool_input'], ensure_ascii=False)}`\n\n")
                
                if trace.get('observations'):
                    f.write("## Результаты\n\n")
                    for o in trace['observations']:
                        status = "" if o.get('success') else ""
                        f.write(f"### {o['id']} {status}\n")
                        f.write(f"{o.get('observation', o.get('error', ''))}\n\n")
                
                if trace.get('final_response'):
                    f.write("## Ответ\n\n")
                    f.write(f"{trace['final_response']['response']}\n")
            
            return str(filename)
        
        return None


# Глобальный экземпляр трекера
tracker = AgentTracker()


def trace_agent(func):
    """Декоратор для автоматического трекинга агентов"""
    def wrapper(agent_name, user_query, *args, **kwargs):
        trace_id = tracker.start_trace(agent_name, user_query)
        
        try:
            result = func(trace_id, user_query, *args, **kwargs)
            
            if isinstance(result, tuple) and len(result) == 2:
                response, success = result
            else:
                response, success = result, True
            
            tracker.end_trace(trace_id, final_response=response, success=success)
            return response
            
        except Exception as e:
            tracker.end_trace(trace_id, success=False, error=str(e))
            raise
    
    return wrapper
