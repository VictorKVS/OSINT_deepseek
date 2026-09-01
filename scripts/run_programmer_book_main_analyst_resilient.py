from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import scripts.run_programmer_book_main_analyst as base


MAX_CONTRACT_ATTEMPTS = 3


def repair_instruction(batch: dict[str, Any], errors: list[str]) -> str:
    allowed_relations = ", ".join(sorted(base.ALLOWED_RELATIONS))
    allowed_decisions = ", ".join(sorted(base.ALLOWED_DECISIONS))
    candidate_ids = [base.review_id(row) for row in batch["candidates"]]
    return (
        "Исправь ТОЛЬКО структуру предыдущего JSON и нарушения контракта. "
        "Не добавляй новые факты и не меняй смысл без необходимости.\n"
        f"Точный batch_id: {batch['batch_id']}\n"
        f"Допустимые candidate_id: {json.dumps(candidate_ids, ensure_ascii=False)}\n"
        f"Допустимые decision: {allowed_decisions}\n"
        f"Допустимые relation.type: {allowed_relations}\n"
        "ВАЖНО: relation.type — это ТОЛЬКО название отношения из списка выше, НИКОГДА не UUID/candidate_id.\n"
        "target_candidate_id — это UUID/candidate_id другого кандидата текущего батча.\n"
        "Если отношение не уверенно — верни пустой массив relations, а не выдумывай тип.\n"
        "Каждый candidate_id должен встретиться в reviews ровно один раз.\n"
        "kb_auto_promotion=false; next_gate=PROFESSOR_REVIEW_REQUIRED.\n"
        f"Ошибки валидатора: {json.dumps(errors, ensure_ascii=False)}\n"
        "Верни только исправленный JSON без markdown."
    )


def _request(
    base_url: str,
    model: str,
    batch: dict[str, Any],
    book_title: str,
    timeout: int,
    previous_result: dict[str, Any] | None,
    errors: list[str] | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    messages: list[dict[str, str]] = [
        {"role": "system", "content": base.SYSTEM_PROMPT},
        {"role": "user", "content": base.build_user_prompt(batch, book_title)},
    ]
    if previous_result is not None and errors:
        messages.append({
            "role": "assistant",
            "content": json.dumps(previous_result, ensure_ascii=False),
        })
        messages.append({
            "role": "user",
            "content": repair_instruction(batch, errors),
        })

    payload = {
        "model": model,
        "temperature": 0.0,
        "messages": messages,
    }
    raw = base.http_json(
        base_url.rstrip("/") + "/chat/completions",
        payload=payload,
        timeout=timeout,
    )
    choices = raw.get("choices") or []
    if not choices:
        raise ValueError("model response has no choices")
    content = str((choices[0].get("message") or {}).get("content") or "")
    usage = raw.get("usage") if isinstance(raw.get("usage"), dict) else {}
    return base.extract_object(content), usage


def call_model_with_contract_repair(
    base_url: str,
    model: str,
    batch: dict[str, Any],
    book_title: str,
    timeout: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    previous: dict[str, Any] | None = None
    errors: list[str] | None = None
    total_usage: dict[str, int] = {}

    for attempt in range(1, MAX_CONTRACT_ATTEMPTS + 1):
        result, usage = _request(
            base_url,
            model,
            batch,
            book_title,
            timeout,
            previous,
            errors,
        )
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            if usage.get(key) is not None:
                total_usage[key] = total_usage.get(key, 0) + int(usage.get(key) or 0)

        errors = base.validate(result, batch)
        if not errors:
            if attempt > 1:
                print(f"contract_repair=PASS batch={batch['batch_id']} attempt={attempt}")
            return result, total_usage or usage

        print(
            f"contract_repair=RETRY batch={batch['batch_id']} "
            f"attempt={attempt}/{MAX_CONTRACT_ATTEMPTS} errors={'; '.join(errors)}"
        )
        previous = result

    raise ValueError("contract repair exhausted: " + "; ".join(errors or []))


def main() -> int:
    # The original runner keeps all resume, metrics, professor-gate and
    # fail-closed semantics. Only the model-call boundary is strengthened.
    base.call_model = call_model_with_contract_repair
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
