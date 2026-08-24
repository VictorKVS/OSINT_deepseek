from father_osint.model_stage_router import ModelCandidate, ModelStageRouter, StagePolicy


def test_deterministic_stage_never_routes_to_model() -> None:
    decision = ModelStageRouter().decide(
        policy=StagePolicy(stage_id="M0", capability="NONE", semantic=False),
        candidates=[ModelCandidate(model_id="x", capability="NONE", quality_score=100)],
        work_item_id="doc-1",
    )
    assert decision.champion is None
    assert decision.reason == "DETERMINISTIC_STAGE"


def test_router_selects_best_eligible_capability_match() -> None:
    decision = ModelStageRouter().decide(
        policy=StagePolicy(stage_id="M6", capability="KNOWLEDGE_EXTRACTION"),
        candidates=[
            ModelCandidate(model_id="weak", capability="KNOWLEDGE_EXTRACTION", quality_score=70),
            ModelCandidate(model_id="wrong", capability="TRANSLATION", quality_score=999),
            ModelCandidate(model_id="best", capability="KNOWLEDGE_EXTRACTION", quality_score=91),
            ModelCandidate(model_id="disabled", capability="KNOWLEDGE_EXTRACTION", quality_score=100, eligible=False),
        ],
        work_item_id="chunk-1",
    )
    assert decision.champion is not None
    assert decision.champion.model_id == "best"


def test_no_model_fails_closed_into_review() -> None:
    decision = ModelStageRouter().decide(
        policy=StagePolicy(stage_id="M8", capability="NLI_VERIFICATION"),
        candidates=[],
        work_item_id="claim-pair-1",
    )
    assert decision.champion is None
    assert decision.human_review_required is True
    assert decision.reason == "NO_ELIGIBLE_MODEL"


def test_close_quality_margin_requests_human_review() -> None:
    decision = ModelStageRouter().decide(
        policy=StagePolicy(
            stage_id="M3",
            capability="EN_RU_TECHNICAL_TRANSLATION",
            human_review_on_close_margin=True,
            close_margin=1.0,
        ),
        candidates=[
            ModelCandidate(model_id="a", capability="EN_RU_TECHNICAL_TRANSLATION", quality_score=95.1),
            ModelCandidate(model_id="b", capability="EN_RU_TECHNICAL_TRANSLATION", quality_score=94.8),
        ],
        work_item_id="book-1",
    )
    assert decision.champion is not None
    assert decision.human_review_required is True
    assert decision.reason == "CLOSE_MARGIN_HUMAN_REVIEW"


def test_full_canary_runs_challenger() -> None:
    decision = ModelStageRouter().decide(
        policy=StagePolicy(
            stage_id="M5",
            capability="TERMINOLOGY_EXTRACTION",
            canary_fraction=1.0,
        ),
        candidates=[
            ModelCandidate(model_id="champ", capability="TERMINOLOGY_EXTRACTION", quality_score=90),
            ModelCandidate(model_id="challenger", capability="TERMINOLOGY_EXTRACTION", quality_score=80),
        ],
        work_item_id="unit-1",
        max_challengers=1,
    )
    assert [item.model_id for item in decision.challengers] == ["challenger"]
