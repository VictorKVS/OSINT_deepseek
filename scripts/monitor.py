#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Мониторинг ресурсов для безопасного запуска LLM
Следит за GPU, RAM, CPU и автоматически подбирает режим работы
"""

import time
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    import psutil
    import GPUtil
    from colorama import init, Fore, Style
    init()
except ImportError as e:
    print(f" Ошибка импорта: {e}")
    print("Установите: pip install psutil gputil colorama")
    exit(1)


class SystemMonitor:
    """Мониторинг системных ресурсов"""
    
    def __init__(self, log_file: str = "logs/system_stats.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        self.history = self.load_history()
        self.crashes = 0
        
    def load_history(self) -> List[Dict]:
        """Загружает историю мониторинга"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Сохраняет историю"""
        # Оставляем только последние 100 записей
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def get_gpu_info(self) -> Dict:
        """Получает информацию о GPU"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return {
                    "name": gpu.name,
                    "temperature": gpu.temperature,
                    "load": gpu.load * 100,
                    "memory_used": gpu.memoryUsed,
                    "memory_total": gpu.memoryTotal,
                    "memory_free": gpu.memoryFree,
                    "memory_used_gb": gpu.memoryUsed / 1024,
                    "memory_total_gb": gpu.memoryTotal / 1024,
                    "memory_free_gb": gpu.memoryFree / 1024
                }
        except:
            pass
        return {
            "name": "No GPU",
            "temperature": 0,
            "load": 0,
            "memory_used": 0,
            "memory_total": 0,
            "memory_free": 0,
            "memory_used_gb": 0,
            "memory_total_gb": 0,
            "memory_free_gb": 0
        }
    
    def get_ram_info(self) -> Dict:
        """Получает информацию о RAM"""
        ram = psutil.virtual_memory()
        return {
            "total": ram.total / (1024**3),
            "available": ram.available / (1024**3),
            "used": ram.used / (1024**3),
            "percent": ram.percent
        }
    
    def get_cpu_info(self) -> Dict:
        """Получает информацию о CPU"""
        return {
            "percent": psutil.cpu_percent(interval=0.5),
            "count": psutil.cpu_count(),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else 0
        }
    
    def check_thresholds(self, gpu_info: Dict, ram_info: Dict) -> List[str]:
        """Проверяет превышение порогов"""
        warnings = []
        
        # GPU температура
        if gpu_info["temperature"] > 80:
            warnings.append(f"{Fore.RED} КРИТИЧЕСКАЯ температура GPU: {gpu_info['temperature']}C{Style.RESET_ALL}")
        elif gpu_info["temperature"] > 70:
            warnings.append(f"{Fore.YELLOW} Высокая температура GPU: {gpu_info['temperature']}C{Style.RESET_ALL}")
        
        # GPU память
        if gpu_info["memory_free_gb"] < 2:
            warnings.append(f"{Fore.RED} КРИТИЧЕСКИ мало VRAM: {gpu_info['memory_free_gb']:.1f} GB{Style.RESET_ALL}")
        elif gpu_info["memory_free_gb"] < 4:
            warnings.append(f"{Fore.YELLOW} Мало VRAM: {gpu_info['memory_free_gb']:.1f} GB{Style.RESET_ALL}")
        
        # RAM
        if ram_info["available"] < 4:
            warnings.append(f"{Fore.RED} КРИТИЧЕСКИ мало RAM: {ram_info['available']:.1f} GB{Style.RESET_ALL}")
        elif ram_info["available"] < 8:
            warnings.append(f"{Fore.YELLOW} Мало RAM: {ram_info['available']:.1f} GB{Style.RESET_ALL}")
        
        return warnings
    
    def get_safe_model(self) -> str:
        """Определяет безопасную модель на основе истории и текущего состояния"""
        gpu = self.get_gpu_info()
        ram = self.get_ram_info()
        
        # Анализируем историю сбоев
        recent_crashes = [e for e in self.history if e.get("crash", False)]
        
        if len(recent_crashes) > 2:
            print(f"{Fore.YELLOW} Обнаружено {len(recent_crashes)} недавних сбоев{Style.RESET_ALL}")
            return "llama3.2:1b"  # Самая безопасная
        
        # Проверяем ресурсы
        if gpu["memory_total_gb"] < 6:
            return "llama3.2:1b"
        elif gpu["memory_total_gb"] < 8:
            return "qwen2.5:3b"
        elif gpu["memory_total_gb"] >= 12:
            return "qwen2.5:7b"  # Для 12GB безопаснее начать с qwen2.5:7b, а deepseek пробовать позже
        else:
            return "qwen2.5:3b"
    
    def log_crash(self, model: str, error: str):
        """Логирует сбой"""
        self.crashes += 1
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "crash",
            "model": model,
            "error": str(error),
            "gpu": self.get_gpu_info(),
            "ram": self.get_ram_info()
        }
        self.history.append(entry)
        self.save_history()
        
        print(f"\n{Fore.RED} ЗАФИКСИРОВАН СБОЙ #{self.crashes}{Style.RESET_ALL}")
        print(f"   Модель: {model}")
        print(f"   Ошибка: {error}")
    
    def display_status(self):
        """Отображает текущее состояние"""
        gpu = self.get_gpu_info()
        ram = self.get_ram_info()
        cpu = self.get_cpu_info()
        warnings = self.check_thresholds(gpu, ram)
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    СИСТЕМНЫЙ МОНИТОРИНГ{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # GPU
        print(f"\n{Fore.CYAN} GPU:{Style.RESET_ALL} {gpu['name']}")
        print(f"   Температура: {gpu['temperature']}C")
        print(f"   Нагрузка: {gpu['load']:.1f}%")
        print(f"   Память: {gpu['memory_used_gb']:.1f}/{gpu['memory_total_gb']:.1f} GB ({gpu['memory_free_gb']:.1f} GB свободно)")
        
        # RAM
        print(f"\n{Fore.CYAN} RAM:{Style.RESET_ALL}")
        print(f"   Всего: {ram['total']:.1f} GB")
        print(f"   Доступно: {ram['available']:.1f} GB")
        print(f"   Использовано: {ram['used']:.1f} GB ({ram['percent']}%)")
        
        # CPU
        print(f"\n{Fore.CYAN} CPU:{Style.RESET_ALL}")
        print(f"   Нагрузка: {cpu['percent']}%")
        print(f"   Частота: {cpu['freq']:.0f} MHz")
        
        # Предупреждения
        if warnings:
            print(f"\n{Fore.YELLOW} ПРЕДУПРЕЖДЕНИЯ:{Style.RESET_ALL}")
            for w in warnings:
                print(w)
        
        # Рекомендация
        safe = self.get_safe_model()
        print(f"\n{Fore.GREEN} Рекомендуемая безопасная модель: {safe}{Style.RESET_ALL}")
        
        return safe


def main():
    """Тест мониторинга"""
    monitor = SystemMonitor()
    
    while True:
        monitor.display_status()
        print(f"\n{Fore.CYAN} Обновление каждые 3 секунды. Ctrl+C для выхода{Style.RESET_ALL}")
        time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Мониторинг завершён{Style.RESET_ALL}")
