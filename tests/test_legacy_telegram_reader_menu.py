# -*- coding: utf-8 -*-

import asyncio

import pytest

pytest.importorskip("telethon")
pytest.importorskip("yaml")

from legacy.telegram import simple_reader


def test_menu_text_is_readable_russian_and_zero_exits(monkeypatch, capsys):
    answers = iter(["0"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

    class FakeReader:
        async def connect(self):
            print("Подключено к Telegram")

        async def disconnect(self):
            print("Отключено от Telegram")

        async def read_all(self):
            raise AssertionError("read_all must not run on exit")

        async def read_channel(self, *_args, **_kwargs):
            raise AssertionError("read_channel must not run on exit")

        def print_stats(self):
            raise AssertionError("print_stats must not run on exit")

        async def save_results(self):
            raise AssertionError("save_results must not run on exit")

    monkeypatch.setattr(simple_reader, "TelegramReader", FakeReader)

    asyncio.run(simple_reader.main())

    output = capsys.readouterr().out

    assert "Прочитать все каналы" in output
    assert "Прочитать конкретный канал" in output
    assert "Показать статистику" in output
    assert "Сохранить результаты" in output
    assert "0. Выход" in output
    assert "5. Выход" not in output
    assert "До свидания!" in output
    assert "Отключено от Telegram" in output
    assert "Рџ" not in output
    assert "РЎ" not in output
