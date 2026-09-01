from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from typing import Any, Iterable

_SAFE_TOKEN_RE = re.compile(r"[^A-Z0-9-]+")
_SPACE_RE = re.compile(r"\s+")


def utc_now_iso() -> str:
    """Return an RFC 3339 UTC timestamp accepted by JSON Schema format checkers."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_json(value: Any, *, exclude_fields: Iterable[str] = ()) -> str:
    excluded = set(exclude_fields)
    if isinstance(value, dict):
        value = {key: item for key, item in value.items() if key not in excluded}
    return sha256_text(canonical_json(value))


def safe_token(value: str, *, fallback: str = "ITEM", max_length: int = 48) -> str:
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    text = _SAFE_TOKEN_RE.sub("-", text.upper()).strip("-")
    return (text or fallback)[:max_length].rstrip("-")


def normalize_name(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).casefold()
    text = re.sub(r"[\W_]+", " ", text, flags=re.UNICODE)
    return _SPACE_RE.sub(" ", text).strip()


_RU_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "shch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def transliterate_ru(value: str) -> str:
    result: list[str] = []
    for char in value:
        lower = char.lower()
        translit = _RU_TO_LAT.get(lower, char)
        if char.isupper() and translit:
            translit = translit[0].upper() + translit[1:]
        result.append(translit)
    return "".join(result)
