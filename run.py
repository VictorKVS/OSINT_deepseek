#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OSINT Studio - ФИНАЛЬНАЯ ВЕРСИЯ
Включает:
- Автоматический мониторинг системы
- Трекинг агентов
- Анализ сбоев
- Защиту от перегрузок
"""

import os
import sys
import time
import json
import threading
import subprocess
from datetime import datetime
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent))

try:
    from colorama import init, Fore, Style
    init()
except ImportError:
    # Если colorama нет, создаём заглушки
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        RESET = ""

# Попытка импорта наших модулей
try:
    from core.logger import logger, log_system_periodically
    HAS_LOGGER = True
except ImportError:
    HAS_LOGGER = False
    print(" Модуль logger не найден, мониторинг ограничен")

try:
    from core.agent_tracker import tracker
    HAS_TRACKER = True
except ImportError:
    HAS_TRACKER = False
    print(" Модуль tracker не найден, трекинг отключён")

# Пытаемся импортировать ollama
try:
    import ollama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False
    print(" Ollama не установлена: pip install ollama")


class OSINTStudio:
    """Главный класс запуска OSINT Studio"""
    
    def __init__(self):
        self.running = False
        self.start_time = time.time()
        self.monitor_thread = None
        self.crash_log = Path("logs") / "crashes"
        self.crash_log.mkdir(parents=True, exist_ok=True)
        
    def check_system_after_crash(self):
        """Проверяет, был ли недавний сбой"""
        print(f"\n{Fore.CYAN} ПРОВЕРКА ПОСЛЕ СБОЯ{Style.RESET_ALL}")
        
        # Ищем последний crash-лог
        crash_files = list(Path("logs").glob("crashes/crash_*.txt"))
        if crash_files:
            latest = max(crash_files, key=lambda p: p.stat().st_mtime)
            age = time.time() - latest.stat().st_mtime
            
            if age < 300:  # меньше 5 минут назад
                print(f"{Fore.RED} ОБНАРУЖЕН НЕДАВНИЙ СБОЙ!{Style.RESET_ALL}")
                print(f"   Файл: {latest}")
                print(f"   Время: {datetime.fromtimestamp(latest.stat().st_mtime)}")
                
                # Показываем содержимое
                try:
                    with open(latest, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"\n{Fore.YELLOW}Содержимое лога:{Style.RESET_ALL}")
                        print(content[:500])  # первые 500 символов
                except:
                    pass
                
                print(f"\n{Fore.YELLOW} РЕКОМЕНДАЦИЯ: Запустите безопасный режим (qwen2.5:3b){Style.RESET_ALL}")
                return True
        return False
    
    def start_monitoring(self):
        """Запускает фоновый мониторинг"""
        if not HAS_LOGGER:
            print(f"{Fore.YELLOW} Мониторинг отключён (нет logger){Style.RESET_ALL}")
            return
            
        print(f"{Fore.CYAN} Запуск системы мониторинга...{Style.RESET_ALL}")
        
        def monitor_loop():
            while self.running:
                try:
                    metrics = logger.log_system_metrics()
                    
                    # Проверяем критические значения
                    warnings = []
                    if metrics.gpu_temp > 80:
                        warnings.append(f" Критическая температура GPU: {metrics.gpu_temp}C")
                    if metrics.gpu_memory_free_gb < 1:
                        warnings.append(f" Критически мало VRAM: {metrics.gpu_memory_free_gb:.1f} GB")
                    if metrics.ram_available_gb < 2:
                        warnings.append(f" Критически мало RAM: {metrics.ram_available_gb:.1f} GB")
                    
                    if warnings and self.running:
                        print(f"\n{Fore.RED}{'='*60}{Style.RESET_ALL}")
                        for w in warnings:
                            print(f"{Fore.RED} {w}{Style.RESET_ALL}")
                        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
                        
                        # Автоматическое снижение риска
                        if metrics.gpu_temp > 85:
                            print(f"{Fore.YELLOW} Аварийное завершение для защиты оборудования{Style.RESET_ALL}")
                            self.running = False
                            os._exit(1)
                    
                    # Периодический статус (каждые 30 секунд)
                    if int(time.time()) % 30 < 5:
                        print(f"\n{Fore.CYAN} СТАТУС:{Style.RESET_ALL}")
                        print(f"   GPU: {metrics.gpu_temp}C, {metrics.gpu_memory_free_gb:.1f} GB свободно")
                        print(f"   RAM: {metrics.ram_available_gb:.1f} GB свободно")
                        print(f"   CPU: {metrics.cpu_percent}%")
                        
                except Exception as e:
                    if self.running:
                        print(f"{Fore.RED} Ошибка мониторинга: {e}{Style.RESET_ALL}")
                
                time.sleep(5)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"{Fore.GREEN} Мониторинг запущен{Style.RESET_ALL}")
    
    def check_system(self):
        """Проверяет систему перед запуском"""
        print(f"\n{Fore.CYAN} ПРОВЕРКА СИСТЕМЫ{Style.RESET_ALL}")
        
        # Проверяем Ollama
        if HAS_OLLAMA:
            try:
                models = ollama.list()
                print(f"{Fore.GREEN} Ollama доступна{Style.RESET_ALL}")
                
                # Показываем модели
                if 'models' in models and models['models']:
                    print(f"   Доступные модели:")
                    safe_model = None
                    for m in models['models']:
                        name = m.get('name', m.get('model', 'unknown'))
                        size_gb = m.get('size', 0) / (1024**3)
                        safe = "" if size_gb < 5 else ""
                        print(f"   {safe} {name} ({size_gb:.1f} GB)")
                        if size_gb < 5 and not safe_model:
                            safe_model = name
                    
                    # Запоминаем безопасную модель
                    if safe_model:
                        self.safe_model = safe_model
                        print(f"\n{Fore.GREEN} Рекомендуемая безопасная модель: {safe_model}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}    Нет загруженных моделей{Style.RESET_ALL}")
                    
            except Exception as e:
                print(f"{Fore.RED} Ollama недоступна: {e}{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.RED} Ollama не установлена{Style.RESET_ALL}")
            return False
        
        return True
    
    def show_menu(self):
        """Показывает меню выбора"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    OSINT STUDIO - ВЫБОР РЕЖИМА{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN} Доступные режимы:{Style.RESET_ALL}")
        print(f"   1. {Fore.GREEN}Мониторинг только{Style.RESET_ALL} - следить за системой")
        print(f"   2. {Fore.BLUE}Умный агент{Style.RESET_ALL} - с трекингом и защитой")
        print(f"   3. {Fore.MAGENTA}RTX 3060 агент{Style.RESET_ALL} - оптимизированный")
        print(f"   4. {Fore.YELLOW}Deepseek safe{Style.RESET_ALL} - для сложных задач")
        print(f"   5. {Fore.CYAN}Анализ сбоев{Style.RESET_ALL} - просмотр логов")
        print(f"   6. {Fore.RED}Выход{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}Ваш выбор (1-6): {Style.RESET_ALL}").strip()
                if choice in ['1', '2', '3', '4', '5', '6']:
                    return choice
                print(f"{Fore.RED}Неверный выбор{Style.RESET_ALL}")
            except KeyboardInterrupt:
                return '6'
    
    def show_crash_logs(self):
        """Показывает логи сбоев"""
        print(f"\n{Fore.CYAN} АНАЛИЗ СБОЕВ{Style.RESET_ALL}")
        
        crash_dir = Path("logs") / "crashes"
        if not crash_dir.exists():
            print(f"{Fore.YELLOW}Нет логов сбоев{Style.RESET_ALL}")
            return
        
        files = list(crash_dir.glob("crash_*.txt"))
        if not files:
            print(f"{Fore.YELLOW}Нет логов сбоев{Style.RESET_ALL}")
            return
        
        # Сортируем по времени
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        
        print(f"{Fore.CYAN}Последние сбои:{Style.RESET_ALL}")
        for i, f in enumerate(files[:5], 1):
            size = f.stat().st_size
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            print(f"   {i}. {mtime} - {f.name} ({size} bytes)")
        
        choice = input(f"\n{Fore.YELLOW}Введите номер для просмотра (Enter - выход): {Style.RESET_ALL}").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            idx = int(choice) - 1
            with open(files[idx], 'r', encoding='utf-8') as f:
                print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
                print(f.read())
                print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        input(f"{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")
    
    def run_agent(self, script_name):
        """Запускает агента с защитой"""
        script_path = Path("scripts") / script_name
        
        if not script_path.exists():
            print(f"{Fore.RED} Скрипт {script_name} не найден{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN} Запуск {script_name}...{Style.RESET_ALL}")
        print(f"{Fore.CYAN} Мониторинг активен{Style.RESET_ALL}")
        print(f"{Fore.YELLOW} Для остановки нажмите Ctrl+C{Style.RESET_ALL}\n")
        
        try:
            # Запускаем агента
            result = subprocess.run([sys.executable, str(script_path)])
            
            if result.returncode != 0:
                print(f"{Fore.RED} Агент завершился с ошибкой{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW} Агент остановлен{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED} Ошибка запуска: {e}{Style.RESET_ALL}")
            # Логируем сбой
            self.log_crash(script_name, str(e))
    
    def log_crash(self, script, error):
        """Логирует сбой"""
        crash_file = self.crash_log / f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(crash_file, 'w', encoding='utf-8') as f:
            f.write(f"СБОЙ: {datetime.now()}\n")
            f.write(f"Скрипт: {script}\n")
            f.write(f"Ошибка: {error}\n")
        print(f"{Fore.RED} Сбой залогирован: {crash_file}{Style.RESET_ALL}")
    
    def monitoring_only(self):
        """Режим только мониторинга"""
        print(f"\n{Fore.GREEN} Режим мониторинга. Нажмите Ctrl+C для выхода{Style.RESET_ALL}")
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Мониторинг остановлен{Style.RESET_ALL}")
    
    def run(self):
        """Главный цикл программы"""
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    OSINT STUDIO - ФИНАЛЬНАЯ ВЕРСИЯ{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        self.running = True
        
        # Проверяем наличие сбоев
        self.check_system_after_crash()
        
        # Запускаем мониторинг
        self.start_monitoring()
        
        # Проверяем систему
        if not self.check_system():
            self.running = False
            input(f"{Fore.YELLOW}Нажмите Enter для выхода...{Style.RESET_ALL}")
            return 1
        
        # Основной цикл
        while self.running:
            try:
                choice = self.show_menu()
                
                if choice == '1':
                    self.monitoring_only()
                
                elif choice == '2':
                    self.run_agent("smart_agent.py")
                
                elif choice == '3':
                    self.run_agent("rtx3060_agent.py")
                
                elif choice == '4':
                    self.run_agent("deepseek_safe.py")
                
                elif choice == '5':
                    self.show_crash_logs()
                
                elif choice == '6':
                    print(f"\n{Fore.GREEN}До свидания!{Style.RESET_ALL}")
                    self.running = False
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Завершение работы...{Style.RESET_ALL}")
                self.running = False
        
        # Итоговая статистика
        elapsed = time.time() - self.start_time
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    РАБОТА ЗАВЕРШЕНА{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"   Время работы: {elapsed:.0f} сек")
        print(f"\n{Fore.GREEN} Логи сохранены в папке logs/{Style.RESET_ALL}")
        
        return 0


def main():
    studio = OSINTStudio()
    sys.exit(studio.run())


if __name__ == "__main__":
    main()
