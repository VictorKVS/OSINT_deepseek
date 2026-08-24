import json
from pathlib import Path


def test_global_brand_standard_requires_top_mark_on_all_sites():
    payload = json.loads(Path("config/ui_brand_standard.json").read_text(encoding="utf-8"))
    assert payload["scope"] == "ALL_FATHER_SITES_AND_WEB_APPS"
    rules = payload["rules"]
    assert rules["top_brand_mark_required"] is True
    assert rules["preferred_placement"] == "TOP_LEFT"
    assert rules["visible_on_mobile"] is True
    assert rules["home_link_required"] is True
    assert rules["accessible_name_required"] is True
    assert rules["plain_text_without_mark_is_not_enough"] is True


def test_osint_control_center_implements_required_brand_mark():
    html = Path("osint_web/static/index.html").read_text(encoding="utf-8")
    svg = Path("osint_web/static/brand-mark.svg").read_text(encoding="utf-8")
    assert html.count('data-brand-mark="required"') >= 2
    assert 'src="/brand-mark.svg"' in html
    assert 'rel="icon"' in html and 'href="/brand-mark.svg"' in html
    assert 'class="top-brand"' in html
    assert 'href="/"' in html
    assert 'aria-label="FATHER' in html
    assert "<svg" in svg and ">FATHER<" in svg


def test_brand_rule_is_documented_as_showcase_acceptance_gate():
    text = Path("docs/UI_BRAND_STANDARD.md").read_text(encoding="utf-8")
    assert "Every FATHER site must have a visible brand mark/icon" in text
    assert "no FATHER showcase page is accepted" in text
