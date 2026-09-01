import hashlib
import json

import pytest

from father_osint.course_compiler import (
    COURSE_PARSER_VERSION,
    CourseCompilerError,
    compile_course_material,
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_markdown_material_preserves_heading_structure_and_chunks():
    data = (
        "# C4 Model\n\nOverview text.\n\n"
        "## Context\n\nSystem context guidance.\n\n"
        "## Container\n\nContainer guidance.\n"
    ).encode("utf-8")

    result = compile_course_material(
        document_id="OTUS-L06-C4",
        version_id="v1",
        artifact_sha256=digest(data),
        data=data,
        mime_type="text/markdown",
        file_name="c4.md",
        max_chunk_chars=600,
    )

    sections = [node for node in result.structure_nodes if node.node_type == "SECTION"]
    assert [node.title for node in sections] == ["C4 Model", "Context", "Container"]
    assert len(result.chunks) == 3
    assert all(chunk.artifact_sha256 == digest(data) for chunk in result.chunks)
    assert result.parser_version == COURSE_PARSER_VERSION


def test_html_headings_are_converted_to_course_structure():
    data = b"<html><body><h1>RAG</h1><p>Intro</p><h2>Retrieval</h2><p>Search first.</p></body></html>"

    result = compile_course_material(
        document_id="OTUS-L07-RAG",
        version_id="v1",
        artifact_sha256=digest(data),
        data=data,
        mime_type="text/html",
        file_name="rag.html",
    )

    sections = [node for node in result.structure_nodes if node.node_type == "SECTION"]
    assert [node.title for node in sections] == ["RAG", "Retrieval"]
    assert any("Search first." in chunk.text for chunk in result.chunks)


def test_ipynb_preserves_markdown_and_code_cells_as_reviewable_chunks():
    notebook = {
        "cells": [
            {"cell_type": "markdown", "source": ["# Semantic cache\n", "Intro text"]},
            {"cell_type": "code", "source": ["print('hello')\n"]},
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    data = json.dumps(notebook).encode("utf-8")

    result = compile_course_material(
        document_id="OTUS-L24-NB",
        version_id="v1",
        artifact_sha256=digest(data),
        data=data,
        mime_type="application/x-ipynb+json",
        file_name="practice.ipynb",
    )

    titles = [node.title for node in result.structure_nodes if node.node_type == "SECTION"]
    assert titles == ["Semantic cache", "Code cell 2"]
    assert any("print('hello')" in chunk.text for chunk in result.chunks)


def test_plain_text_without_headings_uses_body_fallback():
    data = "Architecture debt notes without markdown headings.".encode("utf-8")

    result = compile_course_material(
        document_id="OTUS-L10-TXT",
        version_id="v1",
        artifact_sha256=digest(data),
        data=data,
        mime_type="text/plain",
        file_name="lesson.txt",
    )

    bodies = [node for node in result.structure_nodes if node.node_type == "BODY"]
    assert len(bodies) == 1
    assert result.warnings == ("no headings detected; fallback BODY structure created",)


def test_hash_mismatch_blocks_course_compilation():
    data = b"# Lesson\nText"
    with pytest.raises(CourseCompilerError, match="SHA-256"):
        compile_course_material(
            document_id="OTUS-X",
            version_id="v1",
            artifact_sha256="0" * 64,
            data=data,
            mime_type="text/markdown",
            file_name="lesson.md",
        )


def test_unsupported_pdf_is_explicit_for_next_adapter():
    data = b"%PDF-1.7\nnot-a-real-pdf"
    with pytest.raises(CourseCompilerError, match="unsupported course parser MIME"):
        compile_course_material(
            document_id="OTUS-PDF",
            version_id="v1",
            artifact_sha256=digest(data),
            data=data,
            mime_type="application/pdf",
            file_name="lesson.pdf",
        )
