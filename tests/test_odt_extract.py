import io
import zipfile

import pytest

from father_osint.odt_extract import OdtExtractionError, extract_odt_text


def _odt_bytes(content_xml: bytes) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("mimetype", "application/vnd.oasis.opendocument.text")
        archive.writestr("content.xml", content_xml)
    return buffer.getvalue()


def test_odt_extracts_headings_and_paragraphs_without_external_binaries():
    xml = b'''<?xml version="1.0" encoding="UTF-8"?>
    <office:document-content
      xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
      xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
      <office:body><office:text>
        <text:h>Federal law N 152</text:h>
        <text:p>Personal data</text:p>
        <text:p>Amendment history line</text:p>
      </office:text></office:body>
    </office:document-content>'''
    text = extract_odt_text(_odt_bytes(xml))
    assert text.splitlines() == [
        "Federal law N 152",
        "Personal data",
        "Amendment history line",
    ]


def test_odt_rejects_invalid_zip():
    with pytest.raises(OdtExtractionError, match="valid ZIP"):
        extract_odt_text(b"not-an-odt")


def test_odt_rejects_missing_content_xml():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("mimetype", "application/vnd.oasis.opendocument.text")
    with pytest.raises(OdtExtractionError, match="content.xml is missing"):
        extract_odt_text(buffer.getvalue())


def test_odt_content_xml_size_is_bounded():
    xml = b"<root>" + (b"x" * 200) + b"</root>"
    with pytest.raises(OdtExtractionError, match="exceeds"):
        extract_odt_text(_odt_bytes(xml), max_content_xml_bytes=100)
