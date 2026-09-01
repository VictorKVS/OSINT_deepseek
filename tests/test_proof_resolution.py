from __future__ import annotations

import hashlib
import json
from pathlib import Path

from father_osint.proof_resolution import (
    EVIDENCE_KIND,
    IDENTITY_METHOD,
    resolve_local_official_proof,
    resolve_pack_from_files,
)


def _fixture_html() -> bytes:
    return (
        '<html><body>'
        '<h1>Федеральный закон о <span>персональных данных</span></h1>'
        '<p>Дата подписания: <b>27.07.2006</b></p>'
        '<p>Статья 3. Основные понятия, используемые в настоящем Федеральном законе</p>'
        '</body></html>'
    ).encode('utf-8')


def test_local_proof_uses_visible_text_hash_and_primary_secondary_markers(tmp_path: Path):
    repo = tmp_path
    local = repo / 'data' / 'capture.html'
    local.parent.mkdir(parents=True)
    data = _fixture_html()
    local.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()

    result = resolve_local_official_proof(
        repo_root=repo,
        review_item={'document_id': 'DOC1', 'artifact_sha256': digest},
        source_item={
            'document_id': 'DOC1',
            'primary_identity_markers': [
                'Федеральный закон о персональных данных',
                'Дата подписания: 27.07.2006',
                'Статья 3. Основные понятия, используемые в настоящем Федеральном законе',
            ],
            'identity_markers': ['О персональных данных'],
            'publication_anchor': {'trust_tier': 'A0_OFFICIAL_PUBLICATION'},
        },
        local_path=local,
    )

    assert result.proof_available is True
    assert result.sha256_match is True
    assert result.identity_pass is True
    assert result.identity_method == IDENTITY_METHOD
    assert result.evidence_kind == EVIDENCE_KIND
    assert result.network_used is False
    assert result.new_d2_d3_promotion is False
    assert result.legal_truth_promoted is False


def test_local_proof_fails_closed_on_hash_mismatch(tmp_path: Path):
    local = tmp_path / 'capture.html'
    local.write_bytes(_fixture_html())
    result = resolve_local_official_proof(
        repo_root=tmp_path,
        review_item={'document_id': 'DOC1', 'artifact_sha256': '0' * 64},
        source_item={
            'document_id': 'DOC1',
            'primary_identity_markers': ['Федеральный закон о персональных данных'],
            'identity_markers': ['О персональных данных'],
        },
        local_path=local,
    )
    assert result.proof_available is False
    assert result.sha256_match is False
    assert result.identity_pass is True


def test_pack_resolution_is_network_independent_and_all_or_blocked(tmp_path: Path):
    local_dir = tmp_path / 'data'
    local_dir.mkdir()
    data = _fixture_html()
    digest = hashlib.sha256(data).hexdigest()
    for document_id in ('DOC1', 'DOC2'):
        (local_dir / f'{document_id}.html').write_bytes(data)

    review_path = tmp_path / 'review.json'
    review_path.write_text(json.dumps({'documents': [
        {'document_id': 'DOC1', 'artifact_sha256': digest},
        {'document_id': 'DOC2', 'artifact_sha256': digest},
    ]}), encoding='utf-8')
    source_path = tmp_path / 'pack.json'
    source_path.write_text(json.dumps({'pack_id': 'P', 'documents': [
        {
            'document_id': 'DOC1',
            'primary_identity_markers': ['Федеральный закон о персональных данных'],
            'identity_markers': ['О персональных данных'],
        },
        {
            'document_id': 'DOC2',
            'primary_identity_markers': ['Федеральный закон о персональных данных'],
            'identity_markers': ['О персональных данных'],
        },
    ]}), encoding='utf-8')

    result = resolve_pack_from_files(
        repo_root=tmp_path,
        review_path=review_path,
        source_pack_path=source_path,
        local_dir=local_dir,
    )
    assert result['documents_total'] == 2
    assert result['proof_available'] == 2
    assert result['proof_blocked'] == 0
    assert result['all_proofs_available'] is True
    assert result['network_used'] is False
    assert result['api_required_for_serving'] is False
