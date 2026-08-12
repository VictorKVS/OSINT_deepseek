# -*- coding: utf-8 -*-

from collections import Counter

import pytest

pytest.importorskip("telethon")
pytest.importorskip("yaml")

from legacy.telegram.simple_reader import TelegramReader


def test_analyze_message_accepts_russian_words():
    reader = TelegramReader.__new__(TelegramReader)
    reader.stats = {
        "top_words": Counter(),
        "top_hashtags": Counter(),
    }

    reader.analyze_message("Сегодня Telegram анализирует русские сообщения #осинт")

    assert "сегодня" in reader.stats["top_words"]
    assert "telegram" in reader.stats["top_words"]
    assert "анализирует" in reader.stats["top_words"]
    assert "русские" in reader.stats["top_words"]
    assert "сообщения" in reader.stats["top_words"]
    assert "осинт" in reader.stats["top_hashtags"]
