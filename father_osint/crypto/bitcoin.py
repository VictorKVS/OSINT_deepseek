from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Callable, Iterable, Mapping


class EvidenceConflict(ValueError):
    """Raised when independently sourced deterministic evidence disagrees."""


@dataclass(frozen=True, slots=True)
class AddressStats:
    tx_count: int
    funded_txo_count: int
    funded_txo_sum: int
    spent_txo_count: int
    spent_txo_sum: int
    final_balance: int = 0


@dataclass(frozen=True, slots=True)
class ServiceRow:
    direction: str
    txid: str
    date: str
    wallet_net_btc: float


@dataclass(frozen=True, slots=True)
class FlowBreakdown:
    wallet_input_sat: int
    wallet_output_sat: int
    wallet_delta_sat: int
    direct_service_outflow_sat: int
    verified_service_inflow_sat: int
    other_external_outflow_sat: int
    fee_sat: int
    mixed_destination: bool
    mixed_source: bool


@dataclass(frozen=True, slots=True)
class TraceState:
    tracked_sat: int
    confidence: float = 1.0
    depth: int = 0
    contaminated: bool = False
    stop_reason: str | None = None


def _int(value: Any) -> int:
    if value is None:
        return 0
    return int(value)


def _extract_normalized_stats(payload: Mapping[str, Any]) -> AddressStats:
    """Normalize common Blockstream/mempool or blockchain.info address payloads."""
    if "chain_stats" in payload:
        chain = payload["chain_stats"]
        return AddressStats(
            tx_count=_int(chain.get("tx_count")),
            funded_txo_count=_int(chain.get("funded_txo_count")),
            funded_txo_sum=_int(chain.get("funded_txo_sum")),
            spent_txo_count=_int(chain.get("spent_txo_count")),
            spent_txo_sum=_int(chain.get("spent_txo_sum")),
            final_balance=_int(chain.get("funded_txo_sum")) - _int(chain.get("spent_txo_sum")),
        )
    if "n_tx" in payload:
        return AddressStats(
            tx_count=_int(payload.get("n_tx")),
            funded_txo_count=_int(payload.get("funded_txo_count")),
            funded_txo_sum=_int(payload.get("total_received")),
            spent_txo_count=_int(payload.get("spent_txo_count")),
            spent_txo_sum=_int(payload.get("total_sent")),
            final_balance=_int(payload.get("final_balance")),
        )
    raise EvidenceConflict("unsupported address statistics payload")


def cross_check_address_stats(
    source_payloads: Mapping[str, Mapping[str, Any]],
    *,
    minimum_sources: int = 2,
) -> AddressStats:
    """Require deterministic address totals to agree across independent sources.

    funded/spent output counts are compared only when all sources expose them.
    This lets a blockchain.info-style payload cross-check totals against an
    Esplora-style payload without inventing missing output-count fields.
    """
    if len(source_payloads) < minimum_sources:
        raise EvidenceConflict(f"need at least {minimum_sources} independent sources")
    normalized = {name: _extract_normalized_stats(payload) for name, payload in source_payloads.items()}
    baseline_name, baseline = next(iter(normalized.items()))
    for name, stats in normalized.items():
        required_pairs = {
            "tx_count": (baseline.tx_count, stats.tx_count),
            "funded_txo_sum": (baseline.funded_txo_sum, stats.funded_txo_sum),
            "spent_txo_sum": (baseline.spent_txo_sum, stats.spent_txo_sum),
            "final_balance": (baseline.final_balance, stats.final_balance),
        }
        for field, (left, right) in required_pairs.items():
            if left != right:
                raise EvidenceConflict(
                    f"address stats conflict: {baseline_name}.{field}={left} != {name}.{field}={right}"
                )
    counts = [s for s in normalized.values() if s.funded_txo_count or s.spent_txo_count]
    if len(counts) >= 2:
        first = counts[0]
        for stats in counts[1:]:
            if (first.funded_txo_count, first.spent_txo_count) != (
                stats.funded_txo_count,
                stats.spent_txo_count,
            ):
                raise EvidenceConflict("funded/spent output counts disagree")
    return baseline


def parse_wallet_explorer_service_rows(html: str, service_name: str) -> list[ServiceRow]:
    """Parse WalletExplorer service rows without being broken by nested table rows.

    A critical acceptance gate is enforced: if the service label exists in the
    source but no rows can be extracted, fail instead of silently returning an
    apparently successful empty result.
    """
    parts = re.split(r'<tr class="(sent|received)">', html, flags=re.I)
    rows: list[ServiceRow] = []
    for index in range(1, len(parts), 2):
        direction = parts[index].lower()
        body = parts[index + 1]
        if service_name not in body:
            continue
        date_match = re.search(r'<td class="date">([^<]+)</td>', body, re.I)
        tx_match = re.search(r'/txid/([0-9a-f]{64})', body, re.I)
        amount_match = re.search(
            r'<td class="amount diff">\s*(?:<em>)?\s*([+-]?[0-9.]+)',
            body,
            re.I,
        )
        if date_match and tx_match and amount_match:
            rows.append(
                ServiceRow(
                    direction=direction,
                    txid=tx_match.group(1),
                    date=date_match.group(1).strip(),
                    wallet_net_btc=float(amount_match.group(1)),
                )
            )
    if service_name in html and not rows:
        raise EvidenceConflict(
            f"source contains service label {service_name!r}, but parser extracted zero rows"
        )
    return rows


def _prevout(vin: Mapping[str, Any]) -> Mapping[str, Any]:
    return vin.get("prevout") or vin.get("prev_out") or {}


def reconcile_service_flow(
    tx: Mapping[str, Any],
    *,
    wallet_addresses: Iterable[str],
    is_service_address: Callable[[str], bool],
    external_input_is_service: Callable[[str], bool] | None = None,
) -> FlowBreakdown:
    """Separate wallet delta, direct service flow and unrelated co-flows.

    This deliberately prevents the common analytical error of treating an
    aggregator's wallet-level transaction delta as the amount sent to a named
    service when the same transaction has another external destination.
    """
    wallet = set(wallet_addresses)
    wallet_input = 0
    wallet_output = 0
    direct_service_outflow = 0
    other_external_outflow = 0
    external_inputs: list[str] = []

    for vin in tx.get("vin", []):
        prev = _prevout(vin)
        address = prev.get("scriptpubkey_address") or prev.get("addr")
        value = _int(prev.get("value"))
        if address in wallet:
            wallet_input += value
        elif address:
            external_inputs.append(str(address))

    for vout in tx.get("vout", tx.get("out", [])):
        address = vout.get("scriptpubkey_address") or vout.get("addr")
        value = _int(vout.get("value"))
        if address in wallet:
            wallet_output += value
        elif address and is_service_address(str(address)):
            direct_service_outflow += value
        elif address:
            other_external_outflow += value

    mixed_source = False
    verified_service_inflow = 0
    wallet_delta = wallet_output - wallet_input
    if external_inputs and external_input_is_service is not None:
        source_flags = [external_input_is_service(address) for address in external_inputs]
        mixed_source = not all(source_flags)
        if all(source_flags) and wallet_delta > 0:
            verified_service_inflow = wallet_delta

    return FlowBreakdown(
        wallet_input_sat=wallet_input,
        wallet_output_sat=wallet_output,
        wallet_delta_sat=wallet_delta,
        direct_service_outflow_sat=direct_service_outflow,
        verified_service_inflow_sat=verified_service_inflow,
        other_external_outflow_sat=other_external_outflow,
        fee_sat=_int(tx.get("fee")),
        mixed_destination=direct_service_outflow > 0 and other_external_outflow > 0,
        mixed_source=mixed_source,
    )


def trace_next_hop(
    state: TraceState,
    *,
    forwarded_sat: int,
    unrelated_input_sat: int = 0,
    labeled_service_reached: bool = False,
    repeated_behavior_reached: bool = False,
    max_depth: int = 6,
) -> TraceState:
    """Advance a coin-flow trace while degrading confidence after mixing.

    Confidence is intentionally conservative. The function does not claim
    exact UTXO ancestry after mixing; it makes the uncertainty explicit so a
    downstream report cannot silently back-propagate late wallet activity.
    """
    if state.stop_reason:
        return state
    forwarded = max(0, min(int(forwarded_sat), state.tracked_sat + max(0, int(unrelated_input_sat))))
    confidence = state.confidence
    contaminated = state.contaminated or unrelated_input_sat > 0
    if unrelated_input_sat > 0:
        denominator = state.tracked_sat + unrelated_input_sat
        provenance_share = (state.tracked_sat / denominator) if denominator else 0.0
        confidence *= provenance_share
        confidence *= 0.85
    depth = state.depth + 1
    stop_reason = None
    if labeled_service_reached:
        stop_reason = "labeled_service"
    elif repeated_behavior_reached:
        stop_reason = "repeated_behavior"
    elif depth >= max_depth:
        stop_reason = "max_depth"
    return TraceState(
        tracked_sat=forwarded,
        confidence=max(0.0, min(1.0, confidence)),
        depth=depth,
        contaminated=contaminated,
        stop_reason=stop_reason,
    )
