"""Evidence-safe cryptocurrency analysis primitives.

The package intentionally separates deterministic on-chain observations from
heuristic attribution. Network collectors can feed these pure functions while
tests remain fully offline and reproducible.
"""

from .bitcoin import (
    AddressStats,
    EvidenceConflict,
    FlowBreakdown,
    ServiceRow,
    TraceState,
    cross_check_address_stats,
    parse_wallet_explorer_service_rows,
    reconcile_service_flow,
    trace_next_hop,
)

__all__ = [
    "AddressStats",
    "EvidenceConflict",
    "FlowBreakdown",
    "ServiceRow",
    "TraceState",
    "cross_check_address_stats",
    "parse_wallet_explorer_service_rows",
    "reconcile_service_flow",
    "trace_next_hop",
]
