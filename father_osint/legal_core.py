from __future__ import annotations

import re


class LegalCoreExtractionError(RuntimeError):
    pass


_152_HEADER_RE = re.compile(
    r"Федеральный\s+закон\s+от\s+27\s+июля\s+2006\s+г\.?\s*"
    r"(?:N|№)\s*152(?:\s*[-–—]?\s*)ФЗ",
    re.IGNORECASE,
)
_152_TITLE_RE = re.compile(r"О\s+персональных\s+данных", re.IGNORECASE)
_152_LAST_ARTICLE_RE = re.compile(r"(?m)^Статья\s+25\.?\b", re.IGNORECASE)
_152_SIGNATURE_RE = re.compile(r"(?m)^Президент\s+Российской\s+Федерации\b", re.IGNORECASE)


def is_152_fz_primary_document(text: str) -> bool:
    """Require the actual 152-FZ header/title near the start of the artifact.

    A mere reference to 152-FZ somewhere in commentary/related materials must
    not pass the identity gate for an edition capture.
    """

    normalized = text.replace("\xa0", " ")
    head = normalized[:12_000]
    header = _152_HEADER_RE.search(head)
    if not header:
        return False
    title = _152_TITLE_RE.search(head, header.end())
    return bool(title and title.start() - header.end() <= 2_000)


def extract_152_fz_core_text(text: str) -> str:
    """Extract only the primary 152-FZ legal body from a GARANT working copy.

    The returned scope begins at the exact law header and ends before the
    presidential signature. This intentionally excludes GARANT navigation,
    annotations, news, related documents and other surrounding material.
    """

    normalized = text.replace("\xa0", " ")
    header = _152_HEADER_RE.search(normalized)
    if not header:
        raise LegalCoreExtractionError("152-FZ primary header not found")

    title = _152_TITLE_RE.search(normalized, header.end())
    if not title or title.start() - header.end() > 2_000:
        raise LegalCoreExtractionError("152-FZ title not found near primary header")

    last_article = _152_LAST_ARTICLE_RE.search(normalized, title.end())
    if not last_article:
        raise LegalCoreExtractionError("152-FZ article 25 boundary not found")

    signature = _152_SIGNATURE_RE.search(normalized, last_article.end())
    if not signature:
        raise LegalCoreExtractionError("152-FZ presidential signature boundary not found")

    core = normalized[header.start():signature.start()].strip()
    if len(core) < 5_000:
        raise LegalCoreExtractionError("152-FZ extracted core is implausibly small")
    return core
