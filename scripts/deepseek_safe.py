#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Плавный запуск deepseek-r1:7b с контролем нагрузки
"""

import sys
import time
import os
import psutil
import ollama
from colorama import init, Fore, Style

init()

def print_slow(text, delay=0.03):
    """Печатает текст с задержкой (для эффекта)"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def check_temperature():
    """Проверяет температуру GPU (упрощённо)"""
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            temp = gpus[0].temperature
            print(f"{Fore.CYAN} Температура GPU: {temp}C{Style.RESET_ALL}")
            if temp > 80:
                print(f"{Fore.RED} Высокая температура! Дайте карте остыть.{Style.RESET_ALL}")
                return False
    except:
        pass
    return True

def main():
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    ПЛАВНЫЙ ЗАПУСК DEEPSEEK{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    # Проверка температуры
    if not check_temperature():
        return 1
    
    print(f"{Fore.YELLOW}  ВНИМАНИЕ: deepseek-r1:7b требует много памяти{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Сейчас модель будет загружаться ПОСТЕПЕННО...{Style.RESET_ALL}\n")
    
    time.sleep(3)
    
    # ШАГ 1: Просто проверяем, что модель существует
    print(f"{Fore.CYAN} Шаг 1/4: Проверка модели...{Style.RESET_ALL}")
    try:
        ollama.show('deepseek-r1:7b')
        print(f"{Fore.GREEN} Модель найдена{Style.RESET_ALL}")
    except:
        print(f"{Fore.RED} Модель не найдена. Скачайте: ollama pull deepseek-r1:7b{Style.RESET_ALL}")
        return 1
    
    time.sleep(2)
    
    # ШАГ 2: Прогрев (короткий запрос)
    print(f"{Fore.CYAN} Шаг 2/4: Прогрев модели...{Style.RESET_ALL}")
    try:
        response = ollama.chat(
            model='deepseek-r1:7b',
            messages=[{'role': 'user', 'content': 'Привет'}],
            options={'num_predict': 10}
        )
        print(f"{Fore.GREEN} Модель прогрета{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED} Ошибка прогрева: {e}{Style.RESET_ALL}")
        return 1
    
    time.sleep(2)
    
    # ШАГ 3: Проверка памяти
    print(f"{Fore.CYAN} Шаг 3/4: Проверка ресурсов...{Style.RESET_ALL}")
    ram = psutil.virtual_memory()
    print(f"   RAM свободно: {ram.available / (1024**3):.1f} GB")
    
    if ram.available < 4 * 1024**3:
        print(f"{Fore.YELLOW} Мало оперативной памяти{Style.RESET_ALL}")
    
    time.sleep(2)
    
    # ШАГ 4: Запуск
    print(f"{Fore.CYAN} Шаг 4/4: Запуск диалога...{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN} Модель готова к работе!{Style.RESET_ALL}")
    print(f"{Fore.CYAN} Начинайте с простых вопросов{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   Если почувствуете, что компьютер тормозит  сразу выйдите (exit){Style.RESET_ALL}\n")
    
    messages = []
    while True:
        try:
            user_input = input(f"{Fore.YELLOW}Вы: {Style.RESET_ALL}")
            
            if user_input.lower() in ['exit', 'quit', 'выход']:
                break
            
            if not user_input.strip():
                continue
            
            messages.append({'role': 'user', 'content': user_input})
            
            print(f"{Fore.CYAN} Думаю...{Style.RESET_ALL}")
            
            response = ollama.chat(
                model='deepseek-r1:7b',
                messages=messages,
                options={
                    'temperature': 0.7,
                    'num_predict': 512,  # ограничиваем длину
                    'num_ctx': 2048       # ограничиваем контекст
                }
            )
            
            answer = response['message']['content']
            print(f"{Fore.GREEN}Ассистент: {answer}{Style.RESET_ALL}\n")
            
            messages.append({'role': 'assistant', 'content': answer})
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}До свидания!{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}{Style.RESET_ALL}")
            print("Попробуйте перезапустить скрипт")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
