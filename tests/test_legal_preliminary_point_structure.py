from father_osint.document_compiler import parse_legal_structure


def test_numbered_points_are_explicit_structure_not_body_fallback():
    text = """
Постановление Правительства Российской Федерации
1. Утвердить прилагаемые требования.
2. Признать утратившим силу прежний акт.
Требования к защите персональных данных
1. Настоящий документ устанавливает требования.
2. Безопасность персональных данных обеспечивается системой защиты.
8. При обработке устанавливаются уровни защищенности.
8.1. Первая специальная мера.
8.2. Вторая специальная мера.
""".strip()

    nodes, warnings = parse_legal_structure("DOC-X", "VER-X", text)

    points = [node for node in nodes if node.node_type == "POINT"]
    assert len(points) == 7
    assert not [node for node in nodes if node.node_type == "BODY"]
    assert warnings == []
    assert points[0].locator == "document/point:1"
    assert points[2].locator == "document/point:1#2"
    assert points[-2].locator == "document/point:8.1"
    assert points[-1].locator == "document/point:8.2"


def test_roman_sections_parent_numbered_points():
    text = """
I. Общие положения
1. Настоящий документ определяет требования.
2. Настоящий документ предназначен для операторов.
II. Состав и содержание мер
5. Для обеспечения уровня необходимо выполнение требований.
6. Для выполнения требования необходимо обеспечить режим.
""".strip()

    nodes, warnings = parse_legal_structure("DOC-Y", "VER-Y", text)

    sections = [node for node in nodes if node.node_type == "SECTION"]
    points = [node for node in nodes if node.node_type == "POINT"]
    assert [node.locator for node in sections] == ["section:I", "section:II"]
    assert points[0].locator == "section:I/point:1"
    assert points[1].locator == "section:I/point:2"
    assert points[2].locator == "section:II/point:5"
    assert points[0].parent_node_id == sections[0].node_id
    assert points[2].parent_node_id == sections[1].node_id
    assert warnings == []


def test_article_documents_keep_article_structure():
    text = """
Глава 1. Общие положения
Статья 1. Сфера действия
Текст статьи.
Статья 2. Цель закона
Другой текст.
""".strip()

    nodes, warnings = parse_legal_structure("DOC-Z", "VER-Z", text)

    assert len([node for node in nodes if node.node_type == "ARTICLE"]) == 2
    assert not [node for node in nodes if node.node_type == "BODY"]
    assert warnings == []
