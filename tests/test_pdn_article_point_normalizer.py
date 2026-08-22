from scripts.normalize_pdn_d4_d5_article_points import normalize_article_point_hierarchy


def _node(node_id, node_type, locator, title, parent, text=""):
    return {
        "node_id": node_id,
        "document_id": "DOC-RU-FZ-152-2006",
        "version_id": "VER-1",
        "node_type": node_type,
        "locator": locator,
        "title": title,
        "text": text,
        "parent_node_id": parent,
        "ordinal": 1,
        "content_sha256": "0" * 64,
        "parser_version": "legal-preliminary-v2",
    }


def test_article_points_are_reparented_and_pre_article_noise_is_removed():
    nodes = [
        _node("root", "DOCUMENT", "document", "Document", None),
        _node("noise", "POINT", "document/point:1", "Пункт 1", "root", "страничная навигация"),
        _node("chapter", "CHAPTER", "chapter:1", "Chapter 1", "root"),
        _node("article", "ARTICLE", "article:3", "Статья 3", "chapter", "Основные понятия"),
        _node("p1", "POINT", "chapter:1/point:1", "Пункт 1", "chapter", "персональные данные"),
        _node("p2", "POINT", "chapter:1/point:2", "Пункт 2", "chapter", "оператор"),
    ]
    chunks = [
        {
            "chunk_id": "noise-chunk",
            "document_id": "DOC-RU-FZ-152-2006",
            "version_id": "VER-1",
            "structure_node_id": "noise",
            "locator": "document/point:1/chunk:1",
            "text": "Пункт 1\nстраничная навигация",
            "content_sha256": "0" * 64,
            "artifact_sha256": "1" * 64,
            "parser_version": "legal-preliminary-v2",
        },
        {
            "chunk_id": "p1-chunk",
            "document_id": "DOC-RU-FZ-152-2006",
            "version_id": "VER-1",
            "structure_node_id": "p1",
            "locator": "chapter:1/point:1/chunk:1",
            "text": "Пункт 1\nперсональные данные",
            "content_sha256": "0" * 64,
            "artifact_sha256": "1" * 64,
            "parser_version": "legal-preliminary-v2",
        },
        {
            "chunk_id": "p2-chunk",
            "document_id": "DOC-RU-FZ-152-2006",
            "version_id": "VER-1",
            "structure_node_id": "p2",
            "locator": "chapter:1/point:2/chunk:1",
            "text": "Пункт 2\nоператор",
            "content_sha256": "0" * 64,
            "artifact_sha256": "1" * 64,
            "parser_version": "legal-preliminary-v2",
        },
    ]

    normalized_nodes, normalized_chunks, stats = normalize_article_point_hierarchy(
        nodes,
        chunks,
        document_id="DOC-RU-FZ-152-2006",
        version_id="VER-1",
    )

    assert "noise" not in {node["node_id"] for node in normalized_nodes}
    points = [node for node in normalized_nodes if node["node_type"] == "POINT"]
    assert [node["locator"] for node in points] == ["article:3/point:1", "article:3/point:2"]
    assert all(node["parent_node_id"] == "article" for node in points)
    assert len(normalized_chunks) == 2
    assert all(chunk["structure_node_id"] in {node["node_id"] for node in points} for chunk in normalized_chunks)
    assert stats["removed_pre_article_points"] == 1
    assert stats["reparented_points"] == 2
    assert stats["points_outside_articles_after"] == 0
