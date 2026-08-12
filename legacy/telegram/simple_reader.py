# -*- coding: utf-8 -*-
#!/usr/bin/env python3

"""Verified legacy Telegram reader.

This module preserves the previously working Telethon-based Telegram collection
path as an explicit fallback/reference implementation while the TDLib transport
continues to evolve.

Secrets are never embedded here. Runtime credentials/configuration are loaded
from the local YAML configuration supplied by the operator.

PyYAML and Telethon are deliberately imported lazily so this isolated legacy
fallback does not expand the frozen core DEV dependency surface merely by being
present in the repository.
"""

import asyncio
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = MODULE_DIR / "config.yaml"
DEFAULT_SESSION_PATH = MODULE_DIR / "reader_session"


class TelegramReader:
    def __init__(self, config_path=None, session_path=None):
        config_path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        session_path = Path(session_path) if session_path else DEFAULT_SESSION_PATH

        self.config_path = config_path
        self.session_path = session_path
        self.config = self.load_config(config_path)
        self.client = None
        self.stats = {
            "total_messages": 0,
            "channels_analyzed": 0,
            "top_words": Counter(),
            "top_hashtags": Counter(),
            "messages_by_hour": Counter(),
            "media_count": 0,
        }

    @staticmethod
    def load_config(config_path):
        """Загружает конфигурацию из UTF-8 YAML."""
        try:
            import yaml
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "PyYAML is required only for live legacy Telegram execution"
            ) from exc

        with open(config_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    async def connect(self):
        """Подключается к Telegram с использованием сохранённой Telethon-сессии."""
        try:
            from telethon import TelegramClient
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Telethon is required only for live legacy Telegram execution"
            ) from exc

        tg_config = self.config["telegram"]
        self.client = TelegramClient(
            str(self.session_path),
            tg_config["api_id"],
            tg_config["api_hash"],
        )
        await self.client.start(phone=tg_config["phone_number"])
        print("Подключено к Telegram")

    async def disconnect(self):
        """Корректно отключается от Telegram."""
        if self.client:
            await self.client.disconnect()
            print("Отключено от Telegram")

    def analyze_message(self, text):
        """Выполняет простой частотный анализ текста сообщения."""
        if not text:
            return

        words = re.findall(r"\b[а-яА-ЯёЁa-zA-Z]{4,}\b", text.lower())
        self.stats["top_words"].update(words)

        hashtags = re.findall(r"#(\w+)", text)
        self.stats["top_hashtags"].update(hashtags)

    async def read_channel(self, channel, limit=50):
        """Читает последние сообщения одного канала."""
        try:
            print("\n" + "-" * 50)
            print(f"Читаю канал: {channel}")

            entity = await self.client.get_entity(channel)
            messages = await self.client.get_messages(entity, limit=limit)

            channel_title = getattr(
                entity,
                "title",
                getattr(entity, "username", str(entity.id)),
            )
            participants_count = getattr(entity, "participants_count", None)
            about = getattr(entity, "about", None)

            print(f"Канал: {channel_title}")
            print(
                f"Подписчики: {participants_count}"
                if participants_count is not None
                else "Подписчики: данные недоступны"
            )
            print(
                f"Описание: {about[:100]}"
                if about
                else "Описание: данные недоступны"
            )

            text_messages = 0
            for message in messages:
                if message.text:
                    text_messages += 1
                    self.stats["total_messages"] += 1
                    self.analyze_message(message.text)

                    if message.date:
                        self.stats["messages_by_hour"][message.date.hour] += 1

                if message.media:
                    self.stats["media_count"] += 1

            self.stats["channels_analyzed"] += 1
            print(f"Текстовых сообщений прочитано: {text_messages}/{limit}")

        except Exception as exc:
            print(f"Ошибка чтения канала {channel}: {exc}")

    async def read_all(self):
        """Читает все каналы из конфигурации."""
        tg_config = self.config["telegram"]
        channels = tg_config["channels"]
        limit = tg_config["collection"]["limit_per_channel"]

        print(f"\nНачинаю чтение каналов: {len(channels)}")
        print(f"Лимит на канал: {limit}")

        for channel in channels:
            await self.read_channel(channel, limit)
            await asyncio.sleep(2)

        print("\nЧтение каналов завершено.")
        self.print_stats()

    def print_stats(self):
        """Выводит накопленную статистику на русском языке."""
        print("\n" + "=" * 50)
        print("ОБЩАЯ СТАТИСТИКА")
        print("=" * 50)
        print(f"Каналов проанализировано: {self.stats['channels_analyzed']}")
        print(f"Текстовых сообщений: {self.stats['total_messages']}")
        print(f"Сообщений с медиа: {self.stats['media_count']}")

        print("\nТОП-10 СЛОВ")
        top_words = self.stats["top_words"].most_common(10)
        if top_words:
            for word, count in top_words:
                print(f"{word}: {count}")
        else:
            print("Нет данных.")

        print("\nТОП-10 ХЭШТЕГОВ")
        top_hashtags = self.stats["top_hashtags"].most_common(10)
        if top_hashtags:
            for tag, count in top_hashtags:
                print(f"#{tag}: {count}")
        else:
            print("Нет данных.")

        print("\nСООБЩЕНИЯ ПО ЧАСАМ")
        has_hour_data = False
        for hour in range(24):
            count = self.stats["messages_by_hour"].get(hour, 0)
            if count > 0:
                has_hour_data = True
                bar = "#" * min(count, 20)
                print(f"{hour:02d}:00 {bar} ({count})")
        if not has_hour_data:
            print("Нет данных.")

        print("=" * 50)

    async def save_results(self):
        """Сохраняет результаты анализа в UTF-8 JSON."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "channels": self.stats["channels_analyzed"],
                "total_messages": self.stats["total_messages"],
                "media_count": self.stats["media_count"],
            },
            "top_words": dict(self.stats["top_words"].most_common(20)),
            "top_hashtags": dict(self.stats["top_hashtags"].most_common(20)),
            "hourly_distribution": dict(self.stats["messages_by_hour"]),
        }

        output_directory = Path("analysis_results")
        output_directory.mkdir(exist_ok=True)
        filename = output_directory / (
            "telegram_analysis_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ".json"
        )

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=2)

        print(f"\nРезультаты сохранены в: {filename}")


async def main():
    """Главное интерактивное меню."""
    reader = TelegramReader()

    try:
        await reader.connect()

        while True:
            print("\n" + "=" * 50)
            print("TELEGRAM READER")
            print("=" * 50)
            print("1. Прочитать все каналы")
            print("2. Прочитать конкретный канал")
            print("3. Показать статистику")
            print("4. Сохранить результаты")
            print("0. Выход")

            choice = input("\nВаш выбор (0-4): ").strip()

            if choice == "1":
                await reader.read_all()
            elif choice == "2":
                channel = input(
                    "Введите ссылку или имя канала "
                    "(например @durov или https://t.me/durov): "
                ).strip()
                limit_text = input(
                    "Сколько сообщений прочитать (по умолчанию 50): "
                ).strip()
                limit = int(limit_text) if limit_text.isdigit() else 50
                if limit <= 0:
                    print("Лимит должен быть больше нуля.")
                    continue
                await reader.read_channel(channel, limit)
            elif choice == "3":
                reader.print_stats()
            elif choice == "4":
                await reader.save_results()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Введите число от 0 до 4.")

    finally:
        await reader.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
