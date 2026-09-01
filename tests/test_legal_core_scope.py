from father_osint.legal_core import (
    LegalCoreExtractionError,
    extract_152_fz_core_text,
    is_152_fz_primary_document,
)


def _sample() -> str:
    body = "Нормативный текст статьи. " * 260
    return f"""
Служебная шапка ГАРАНТа
Федеральный закон от 27 июля 2006 г. N 152-ФЗ
О персональных данных
С изменениями и дополнениями от:
25 ноября 2009 г., 26 июля 2026 г.
Глава 1. Общие положения
Статья 1. Сфера действия настоящего Федерального закона
{body}
Статья 25. Заключительные положения
{body}
Президент Российской Федерации
В. Путин
После подписи: Статья 999. Посторонний материал
4 августа 2026 г.
"""


def test_primary_152_identity_requires_actual_header_and_nearby_title():
    assert is_152_fz_primary_document(_sample()) is True
    assert is_152_fz_primary_document(
        "Справка: Федеральный закон 152-ФЗ регулирует О персональных данных"
    ) is False


def test_152_core_excludes_surrounding_garant_material():
    core = extract_152_fz_core_text(_sample())

    assert core.startswith("Федеральный закон от 27 июля 2006 г. N 152-ФЗ")
    assert "Статья 25. Заключительные положения" in core
    assert "Президент Российской Федерации" not in core
    assert "Статья 999" not in core
    assert "4 августа 2026" not in core


def test_152_core_fails_closed_without_signature_boundary():
    text = _sample().replace("Президент Российской Федерации", "")
    try:
        extract_152_fz_core_text(text)
    except LegalCoreExtractionError as exc:
        assert "signature boundary" in str(exc)
    else:
        raise AssertionError("missing legal-core end boundary must fail closed")
