#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Умный агент с системой самодиагностики и восстановления после сбоев
"""

import sys
import time
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import ollama
    from colorama import init, Fore, Style
    from scripts.monitor import SystemMonitor
    init()
except ImportError as e:
    print(f" Ошибка импорта: {e}")
    print("Установите: pip install ollama colorama psutil gputil")
    sys.exit(1)


class SmartAgent:
    """Агент с самодиагностикой и защитой от сбоев"""
    
    def __init__(self):
        self.monitor = SystemMonitor()
        self.crash_count = 0
        self.current_model = None
        self.max_retries = 3
        
    def select_safe_model(self):
        """Выбирает безопасную модель на основе мониторинга"""
        print(f"\n{Fore.CYAN} Анализ системы...{Style.RESET_ALL}")
        
        # Получаем рекомендацию от монитора
        recommended = self.monitor.get_safe_model()
        
        # Показываем состояние
        self.monitor.display_status()
        
        # Спрашиваем пользователя
        print(f"\n{Fore.CYAN} Доступные режимы:{Style.RESET_ALL}")
        print(f"   1. {Fore.GREEN}Безопасный{Style.RESET_ALL} - {recommended} (рекомендуется)")
        print(f"   2. {Fore.YELLOW}Обычный{Style.RESET_ALL} - qwen2.5:3b")
        print(f"   3. {Fore.RED}Мощный{Style.RESET_ALL} - deepseek-r1:7b (риск сбоя)")
        print(f"   4. {Fore.CYAN}Свой{Style.RESET_ALL} - ввести имя модели")
        
        choice = input(f"\n{Fore.YELLOW}Ваш выбор (1-4): {Style.RESET_ALL}").strip()
        
        models = {
            "1": recommended,
            "2": "qwen2.5:3b",
            "3": "deepseek-r1:7b"
        }
        
        if choice in models:
            self.current_model = models[choice]
        elif choice == "4":
            self.current_model = input("Введите имя модели: ").strip()
        else:
            self.current_model = recommended
        
        # Проверяем, существует ли модель
        try:
            ollama.show(self.current_model)
            print(f"{Fore.GREEN} Модель {self.current_model} доступна{Style.RESET_ALL}")
            return True
        except:
            print(f"{Fore.RED} Модель {self.current_model} не найдена{Style.RESET_ALL}")
            print(f"Скачайте: ollama pull {self.current_model}")
            return False
    
    def chat_with_protection(self):
        """Чат с защитой от сбоев"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    УМНЫЙ АГЕНТ (режим: {self.current_model}){Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW} Система мониторинга активна{Style.RESET_ALL}")
        print(f"   При первых признаках перегрузки агент переключится в безопасный режим\n")
        
        messages = []
        
        while True:
            try:
                # Периодический мониторинг (каждые 30 секунд)
                if len(messages) % 5 == 0 and len(messages) > 0:
                    gpu = self.monitor.get_gpu_info()
                    ram = self.monitor.get_ram_info()
                    warnings = self.monitor.check_thresholds(gpu, ram)
                    
                    if warnings:
                        print(f"\n{Fore.YELLOW} Обнаружены проблемы:{Style.RESET_ALL}")
                        for w in warnings:
                            print(w)
                        
                        if gpu["temperature"] > 80 or gpu["memory_free_gb"] < 1:
                            print(f"{Fore.RED} КРИТИЧЕСКИЙ РЕЖИМ! Переключаюсь на безопасную модель...{Style.RESET_ALL}")
                            self.current_model = self.monitor.get_safe_model()
                            print(f"{Fore.GREEN} Теперь использую: {self.current_model}{Style.RESET_ALL}")
                            messages = []  # Сбрасываем историю для новой модели
                            continue
                
                user_input = input(f"\n{Fore.YELLOW}Вы: {Style.RESET_ALL}")
                
                if user_input.lower() in ['exit', 'quit', 'выход']:
                    break
                    
                if user_input.lower() == '/status':
                    self.monitor.display_status()
                    continue
                
                if not user_input.strip():
                    continue
                
                messages.append({'role': 'user', 'content': user_input})
                
                # Измеряем время ответа
                start = time.time()
                response = ollama.chat(
                    model=self.current_model,
                    messages=messages,
                    options={
                        'temperature': 0.7,
                        'num_predict': 512,
                        'num_ctx': 2048
                    }
                )
                elapsed = time.time() - start
                
                answer = response['message']['content']
                print(f"{Fore.GREEN}Ассистент ({elapsed:.1f}с): {answer}{Style.RESET_ALL}")
                
                messages.append({'role': 'assistant', 'content': answer})
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}До свидания!{Style.RESET_ALL}")
                break
                
            except Exception as e:
                self.crash_count += 1
                self.monitor.log_crash(self.current_model, str(e))
                
                print(f"\n{Fore.RED} ПРОИЗОШЁЛ СБОЙ #{self.crash_count}{Style.RESET_ALL}")
                
                if self.crash_count >= self.max_retries:
                    print(f"{Fore.YELLOW} Слишком много сбоев. Переключаюсь в супербезопасный режим...{Style.RESET_ALL}")
                    self.current_model = "llama3.2:1b"
                    self.crash_count = 0
                    messages = []
                    continue
                
                retry = input(f"{Fore.YELLOW}Повторить с той же моделью? (y/n): {Style.RESET_ALL}").lower()
                if retry != 'y':
                    break
    
    def run(self):
        """Запуск агента"""
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    SMART AGENT - САМОДИАГНОСТИКА{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # Выбираем модель
        if not self.select_safe_model():
            return 1
        
        # Запускаем чат
        self.chat_with_protection()
        
        # Итоговая статистика
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    ИТОГОВАЯ СТАТИСТИКА{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"   Сбоев за сессию: {self.crash_count}")
        print(f"   Финальная модель: {self.current_model}")
        
        # Сохраняем историю
        self.monitor.save_history()
        
        return 0


def main():
    agent = SmartAgent()
    sys.exit(agent.run())


if __name__ == "__main__":
    main()
