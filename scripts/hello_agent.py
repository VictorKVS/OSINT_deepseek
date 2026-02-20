#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Hello Agent - тестовый агент для проверки связи с Ollama
Исправленная версия с лучшей обработкой ошибок
"""

import sys
import time
from pathlib import Path

try:
    import ollama
    from colorama import init, Fore, Style
    init()
except ImportError as e:
    print(f" Ошибка импорта: {e}")
    print("Установите библиотеки: pip install ollama colorama")
    sys.exit(1)


def check_ollama():
    """Проверяет доступность Ollama и возвращает список моделей"""
    try:
        # Пробуем получить список моделей
        response = ollama.list()
        
        # Разные версии Ollama возвращают разные форматы
        models = []
        if 'models' in response:
            # Новая версия
            models = response['models']
        elif isinstance(response, list):
            # Старая версия
            models = response
        else:
            # Неизвестный формат
            print(f"{Fore.YELLOW} Неизвестный формат ответа: {type(response)}{Style.RESET_ALL}")
            return True, []  # Ollama работает, но моделей нет
        
        return True, models
        
    except Exception as e:
        print(f"{Fore.RED} Ошибка подключения к Ollama: {e}{Style.RESET_ALL}")
        return False, []


def main():
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    OSINT DeepSeek - Hello Agent{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    # Шаг 1: Проверяем Ollama
    print(f"{Fore.CYAN} Проверка подключения к Ollama...{Style.RESET_ALL}")
    ollama_ok, models = check_ollama()
    
    if not ollama_ok:
        print(f"\n{Fore.RED} Ollama не запущена или недоступна!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Решение:{Style.RESET_ALL}")
        print("  1. Запустите Ollama (иконка в трее или 'ollama serve' в новом окне)")
        print("  2. Дождитесь, пока Ollama загрузится")
        print("  3. Запустите этот скрипт снова")
        return 1
    
    print(f"{Fore.GREEN} Ollama доступна{Style.RESET_ALL}")
    
    # Шаг 2: Показываем доступные модели
    if models:
        print(f"\n{Fore.CYAN} Доступные модели:{Style.RESET_ALL}")
        for i, model in enumerate(models, 1):
            # Разные версии Ollama хранят имя по-разному
            if isinstance(model, dict):
                name = model.get('name', model.get('model', 'Неизвестно'))
            else:
                name = str(model)
            
            # Пробуем получить размер
            size = ""
            if isinstance(model, dict) and 'size' in model:
                size_gb = model['size'] / (1024**3)
                size = f" ({size_gb:.2f} GB)"
            
            print(f"   {i}. {name}{size}")
    else:
        print(f"\n{Fore.YELLOW} Нет загруженных моделей{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Скачайте модель:{Style.RESET_ALL} ollama pull llama3.2:1b")
        return 1
    
    # Шаг 3: Выбираем модель для диалога
    model_name = "llama3.2:1b"  # По умолчанию
    
    # Проверяем, есть ли такая модель в списке
    available_names = []
    for m in models:
        if isinstance(m, dict):
            available_names.append(m.get('name', ''))
            available_names.append(m.get('model', ''))
        else:
            available_names.append(str(m))
    
    # Если модели llama3.2:1b нет, берём первую доступную
    if not any(model_name in name for name in available_names):
        if models:
            first_model = models[0]
            if isinstance(first_model, dict):
                model_name = first_model.get('name', first_model.get('model', 'unknown'))
            else:
                model_name = str(first_model)
            print(f"{Fore.YELLOW} Модель llama3.2:1b не найдена, использую {model_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED} Нет доступных моделей{Style.RESET_ALL}")
            return 1
    
    # Шаг 4: Простой диалог
    print(f"\n{Fore.GREEN} Всё готово! Использую модель: {model_name}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Напишите сообщение (или 'exit' для выхода){Style.RESET_ALL}\n")
    
    messages = []
    while True:
        try:
            user_input = input(f"{Fore.YELLOW}Вы: {Style.RESET_ALL}")
            
            if user_input.lower() in ['exit', 'quit', 'выход']:
                break
            
            if not user_input.strip():
                continue
            
            messages.append({'role': 'user', 'content': user_input})
            
            # Отправляем запрос с таймаутом
            response = ollama.chat(
                model=model_name,
                messages=messages,
                options={'temperature': 0.7}
            )
            
            answer = response['message']['content']
            print(f"{Fore.GREEN}Ассистент: {answer}{Style.RESET_ALL}\n")
            
            messages.append({'role': 'assistant', 'content': answer})
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}До свидания!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
