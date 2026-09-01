from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ShapeViolation:
    field: str
    code: str
    message: str
    severity: str = "ERROR"


@dataclass(frozen=True, slots=True)
class KnowledgeShape:
    object_type: str
    required_fields: tuple[str, ...] = ()
    non_empty_fields: tuple[str, ...] = ()
    allowed_values: Mapping[str, tuple[Any, ...]] = field(default_factory=dict)
    shape_version: str = "1.0"

    def __post_init__(self) -> None:
        if not self.object_type.strip():
            raise ValueError("shape object_type is required")
        if not self.shape_version.strip():
            raise ValueError("shape_version is required")


def validate_shape(payload: Mapping[str, Any], shape: KnowledgeShape) -> tuple[ShapeViolation, ...]:
    violations: list[ShapeViolation] = []

    for field_name in shape.required_fields:
        if field_name not in payload:
            violations.append(
                ShapeViolation(
                    field=field_name,
                    code="REQUIRED_FIELD_MISSING",
                    message=f"required field {field_name!r} is missing",
                )
            )

    for field_name in shape.non_empty_fields:
        if field_name in payload:
            value = payload[field_name]
            if value is None or value == "" or value == [] or value == () or value == {}:
                violations.append(
                    ShapeViolation(
                        field=field_name,
                        code="NON_EMPTY_REQUIRED",
                        message=f"field {field_name!r} must not be empty",
                    )
                )

    for field_name, allowed in shape.allowed_values.items():
        if field_name in payload and payload[field_name] not in allowed:
            violations.append(
                ShapeViolation(
                    field=field_name,
                    code="VALUE_NOT_ALLOWED",
                    message=f"field {field_name!r} has a value outside the allowed set",
                )
            )

    return tuple(violations)


def require_shape_conformance(payload: Mapping[str, Any], shape: KnowledgeShape) -> None:
    violations = validate_shape(payload, shape)
    errors = [item for item in violations if item.severity == "ERROR"]
    if errors:
        codes = ", ".join(f"{item.field}:{item.code}" for item in errors)
        raise ValueError(f"knowledge object does not conform to {shape.object_type}@{shape.shape_version}: {codes}")


KB_READY_COMMON_SHAPE = KnowledgeShape(
    object_type="KB_READY_COMMON",
    required_fields=(
        "object_id",
        "object_type",
        "scope_id",
        "source_document_id",
        "source_version_id",
        "source_locator",
        "method_version",
        "review_state",
    ),
    non_empty_fields=(
        "object_id",
        "object_type",
        "scope_id",
        "source_document_id",
        "source_version_id",
        "source_locator",
        "method_version",
        "review_state",
    ),
    allowed_values={
        "review_state": ("PASS", "PASS_WITH_LIMITATIONS", "REWORK", "INCONCLUSIVE"),
    },
    shape_version="1.0",
)
