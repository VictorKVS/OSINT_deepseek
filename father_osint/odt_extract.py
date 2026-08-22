from __future__ import annotations

import io
import zipfile
from xml.etree import ElementTree as ET


class OdtExtractionError(RuntimeError):
    pass


_MAX_CONTENT_XML_BYTES = 20_000_000


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def extract_odt_text(data: bytes, *, max_content_xml_bytes: int = _MAX_CONTENT_XML_BYTES) -> str:
    """Extract paragraph/heading text from an ODT without external binaries.

    This is intentionally a bounded, read-only adapter for operator-downloaded
    working copies. It does not execute macros, resolve external references, or
    unpack arbitrary members. Only ``content.xml`` is read.
    """

    if not data:
        raise OdtExtractionError("ODT artifact is empty")
    if max_content_xml_bytes <= 0:
        raise ValueError("max_content_xml_bytes must be > 0")

    try:
        with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
            try:
                info = archive.getinfo("content.xml")
            except KeyError as exc:
                raise OdtExtractionError("ODT content.xml is missing") from exc
            if info.file_size <= 0:
                raise OdtExtractionError("ODT content.xml is empty")
            if info.file_size > max_content_xml_bytes:
                raise OdtExtractionError(
                    f"ODT content.xml exceeds max_content_xml_bytes={max_content_xml_bytes}"
                )
            xml_bytes = archive.read(info)
    except zipfile.BadZipFile as exc:
        raise OdtExtractionError("ODT artifact is not a valid ZIP container") from exc

    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        raise OdtExtractionError(f"ODT content.xml is invalid XML: {exc}") from exc

    blocks: list[str] = []
    for element in root.iter():
        if _local_name(element.tag) not in {"h", "p"}:
            continue
        text = " ".join("".join(element.itertext()).replace("\xa0", " ").split())
        if text:
            blocks.append(text)

    result = "\n".join(blocks).strip()
    if not result:
        raise OdtExtractionError("ODT contains no extractable paragraph/heading text")
    return result
