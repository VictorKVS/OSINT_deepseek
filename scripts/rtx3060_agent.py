#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Оптимизированный скрипт для RTX 3060 12GB
"""

import sys
import time
import ollama
from colorama import init, Fore, Style

init()

MODELS = {
    "1": {"name": "llama3.2:1b", "desc": " Быстрая, для тестов"},
    "2": {"name": "qwen2.5:3b", "desc": " Хороший русский, быстрая"},
    "3": {"name": "deepseek-r1:7b", "desc": " Умная, для сложных задач"},
    "4": {"name": "qwen2.5:7b", "desc": " Альтернатива deepseek"},
    "5": {"name": "custom", "desc": " Своя модель"}
}

def main():
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    ЗАПУСК НА RTX 3060 12GB{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    # Показываем доступные модели
    print(f"\n{Fore.CYAN} Выберите модель:{Style.RESET_ALL}")
    for key, model in MODELS.items():
        print(f"   {key}. {model['desc']} - {model['name']}")
    
    choice = input(f"\n{Fore.YELLOW}Ваш выбор (1-5): {Style.RESET_ALL}").strip()
    
    if choice == "5":
        model_name = input("Введите имя модели: ").strip()
    else:
        model_name = MODELS.get(choice, MODELS["1"])["name"]
    
    print(f"\n{Fore.GREEN} Выбрана модель: {model_name}{Style.RESET_ALL}")
    print(f"{Fore.CYAN} Советы:{Style.RESET_ALL}")
    print("   - Для выхода напишите 'exit'")
    print("   - Для очистки истории напишите 'clear'")
    print("   - Для смены модели перезапустите скрипт\n")
    
    messages = []
    while True:
        try:
            user_input = input(f"{Fore.YELLOW}Вы: {Style.RESET_ALL}")
            
            if user_input.lower() in ['exit', 'quit', 'выход']:
                break
            if user_input.lower() == 'clear':
                messages = []
                print(f"{Fore.GREEN}История очищена{Style.RESET_ALL}\n")
                continue
            if not user_input.strip():
                continue
            
            messages.append({'role': 'user', 'content': user_input})
            
            # Замеряем время
            start = time.time()
            
            response = ollama.chat(
                model=model_name,
                messages=messages,
                options={
                    'temperature': 0.7,
                    'num_predict': 1024,
                    'num_ctx': 4096  # достаточно для большинства задач
                }
            )
            
            elapsed = time.time() - start
            answer = response['message']['content']
            
            print(f"{Fore.GREEN}Ассистент ({elapsed:.1f} сек): {answer}{Style.RESET_ALL}\n")
            
            messages.append({'role': 'assistant', 'content': answer})
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}До свидания!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            print("Если модель не запускается, попробуйте перезапустить Ollama")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
