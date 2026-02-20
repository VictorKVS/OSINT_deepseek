#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Центральная система логирования для OSINT Studio
"""

import os
import json
import time
import psutil
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import csv

try:
    import GPUtil
    HAS_GPU = True
except:
    HAS_GPU = False


@dataclass
class SystemMetrics:
    """Метрики системы"""
    timestamp: str
    cpu_percent: float
    cpu_freq: float
    ram_total_gb: float
    ram_available_gb: float
    ram_percent: float
    disk_usage_percent: float
    gpu_name: str = "No GPU"
    gpu_temp: float = 0
    gpu_load: float = 0
    gpu_memory_total_gb: float = 0
    gpu_memory_used_gb: float = 0
    gpu_memory_free_gb: float = 0


class UnifiedLogger:
    """Единый логгер для всей системы"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Счётчики
        self.total_queries = 0
        self.successful_queries = 0
        self.failed_queries = 0
        self.crash_count = 0
        
        # Настройки предупреждений
        self.warning_thresholds = {
            "gpu_temp": 80,
            "gpu_memory_min": 2,
            "ram_min": 4,
            "cpu_max": 90
        }
    
    def get_system_metrics(self) -> SystemMetrics:
        """Собирает текущие метрики системы"""
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
        
        # RAM
        ram = psutil.virtual_memory()
        
        # Disk
        disk = psutil.disk_usage('/')
        
        # GPU
        gpu_name = "No GPU"
        gpu_temp = 0
        gpu_load = 0
        gpu_memory_total = 0
        gpu_memory_used = 0
        gpu_memory_free = 0
        
        if HAS_GPU:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    gpu_name = gpu.name
                    gpu_temp = gpu.temperature
                    gpu_load = gpu.load * 100
                    gpu_memory_total = gpu.memoryTotal / 1024
                    gpu_memory_used = gpu.memoryUsed / 1024
                    gpu_memory_free = gpu.memoryFree / 1024
            except:
                pass
        
        return SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=cpu_percent,
            cpu_freq=cpu_freq,
            ram_total_gb=ram.total / (1024**3),
            ram_available_gb=ram.available / (1024**3),
            ram_percent=ram.percent,
            disk_usage_percent=disk.percent,
            gpu_name=gpu_name,
            gpu_temp=gpu_temp,
            gpu_load=gpu_load,
            gpu_memory_total_gb=gpu_memory_total,
            gpu_memory_used_gb=gpu_memory_used,
            gpu_memory_free_gb=gpu_memory_free
        )
    
    def log_system_metrics(self) -> SystemMetrics:
        """Записывает системные метрики"""
        metrics = self.get_system_metrics()
        return metrics
    
    def check_warnings(self) -> list:
        """Проверяет текущее состояние на предупреждения"""
        metrics = self.get_system_metrics()
        warnings = []
        
        if metrics.gpu_temp > self.warning_thresholds["gpu_temp"]:
            warnings.append(f" GPU температура: {metrics.gpu_temp}C")
        
        if metrics.gpu_memory_free_gb < self.warning_thresholds["gpu_memory_min"]:
            warnings.append(f" Мало VRAM: {metrics.gpu_memory_free_gb:.1f} GB")
        
        if metrics.ram_available_gb < self.warning_thresholds["ram_min"]:
            warnings.append(f" Мало RAM: {metrics.ram_available_gb:.1f} GB")
        
        return warnings
    
    def get_stats(self) -> dict:
        """Возвращает статистику"""
        return {
            "total_queries": self.total_queries,
            "successful": self.successful_queries,
            "failed": self.failed_queries,
            "crashes": self.crash_count,
            "success_rate": (self.successful_queries / max(1, self.total_queries)) * 100
        }


# Глобальный экземпляр логгера
logger = UnifiedLogger()


def log_system_periodically(interval: int = 10):
    """Запускает периодическое логирование системы"""
    import threading
    
    def _log():
        while True:
            logger.log_system_metrics()
            time.sleep(interval)
    
    thread = threading.Thread(target=_log, daemon=True)
    thread.start()
    return thread
