from __future__ import annotations

import argparse
import json
from pathlib import Path

from .demo import build_demo
from .journal import HashChainJournal
from .models import (
    JurisdictionScope,
    RiskTier,
    ScreeningDepth,
    ScreeningRequest,
    Subject,
    SubjectKind,
)
from .planner import ScreeningPlanner
from .profiles import PROFILES, checks_for_profile
from .sources import SOURCES


def _parse_identifiers(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise argparse.ArgumentTypeError(f"identifier must use key=value: {value}")
        key, item = value.split("=", 1)
        if not key.strip() or not item.strip():
            raise argparse.ArgumentTypeError(f"identifier must use non-empty key=value: {value}")
        result[key.strip()] = item.strip()
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="screening-factory")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="Create a deterministic screening plan")
    plan.add_argument("--kind", choices=[item.value for item in SubjectKind], required=True)
    plan.add_argument("--scope", choices=[item.value for item in JurisdictionScope], required=True)
    plan.add_argument("--country", required=True)
    plan.add_argument("--name", required=True)
    plan.add_argument("--identifier", action="append", default=[])
    plan.add_argument("--dob")
    plan.add_argument("--region", action="append", default=[])
    plan.add_argument("--purpose", required=True)
    plan.add_argument("--legal-basis", required=True)
    plan.add_argument("--depth", choices=[item.value for item in ScreeningDepth], default="STANDARD")
    plan.add_argument("--risk", choices=[item.value for item in RiskTier], default="MEDIUM")
    plan.add_argument("--output", required=True)

    demo = sub.add_parser("demo", help="Run the offline synthetic factory demo")
    demo.add_argument("--output", default="runtime/screening-factory-demo")

    verify = sub.add_parser("verify-journal", help="Verify a hash-chain journal")
    verify.add_argument("path")

    sub.add_parser("catalog", help="Print profiles and source registry summary")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        print(json.dumps(build_demo(args.output), ensure_ascii=False, indent=2))
        return 0
    if args.command == "verify-journal":
        ok, errors = HashChainJournal(args.path).verify()
        print(json.dumps({"verified": ok, "errors": errors}, ensure_ascii=False, indent=2))
        return 0 if ok else 1
    if args.command == "catalog":
        payload = {
            "profiles": {
                profile_id: {
                    "title": profile.title_ru,
                    "checks": len(checks_for_profile(profile)),
                    "source_packs": list(profile.source_pack_ids),
                }
                for profile_id, profile in PROFILES.items()
            },
            "registered_official_source_descriptors": len(SOURCES),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    subject = Subject(
        kind=SubjectKind(args.kind),
        display_name=args.name,
        country_code=args.country,
        identifiers=_parse_identifiers(args.identifier),
        date_of_birth=args.dob,
        known_regions=args.region,
    )
    request = ScreeningRequest(
        subject=subject,
        purpose=args.purpose,
        legal_basis_note=args.legal_basis,
        jurisdiction_scope=JurisdictionScope(args.scope),
        depth=ScreeningDepth(args.depth),
        risk_tier=RiskTier(args.risk),
    )
    plan = ScreeningPlanner().build(request)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
