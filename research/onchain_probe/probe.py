#!/usr/bin/env python3
"""
Read-only public on-chain probe for two OSINT test addresses.

Purpose:
- collect reproducible public blockchain data from several independent sources;
- preserve raw responses with SHA-256 and acquisition timestamps;
- calculate address-level statistics without claiming identity;
- keep all failures visible instead of silently filling gaps.

This is a research-only probe. It does not broadcast transactions, authenticate to
accounts, scan private infrastructure, or use non-public data.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

BTC_ADDRESS = "1CfXQEZFcfje4bPqNbu9dtj2FXufUpqD75"
TRON_ADDRESS = "TVpkbcdFitcVMGX9Ty9g33FNSwTzq49fkF"
TRON_USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6"

USER_AGENT = (
    "OSINT-deepseek-public-chain-probe/0.1 "
    "(read-only research; https://github.com/VictorKVS/OSINT_deepseek)"
)


@dataclass
class FetchRecord:
    source_id: str
    method: str
    url: str
    fetched_at_utc: str
    status: int | None
    content_type: str | None
    byte_length: int
    sha256: str | None
    raw_path: str | None
    error: str | None


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def safe_name(source_id: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in source_id)


class Collector:
    def __init__(self, out_dir: Path, timeout: int = 30, retries: int = 3) -> None:
        self.out_dir = out_dir
        self.raw_dir = out_dir / "raw"
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self.retries = retries
        self.records: list[FetchRecord] = []

    def request_json(
        self,
        source_id: str,
        url: str,
        *,
        method: str = "GET",
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any | None:
        payload = None
        req_headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json,text/plain;q=0.9,*/*;q=0.1",
        }
        if headers:
            req_headers.update(headers)
        if body is not None:
            payload = json.dumps(body, separators=(",", ":")).encode("utf-8")
            req_headers["Content-Type"] = "application/json"

        last_error: str | None = None
        for attempt in range(1, self.retries + 1):
            fetched_at = utcnow()
            try:
                req = urllib.request.Request(
                    url=url, data=payload, headers=req_headers, method=method
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    raw = response.read()
                    status = int(getattr(response, "status", 200))
                    content_type = response.headers.get("Content-Type")
                digest = hashlib.sha256(raw).hexdigest()
                path = self.raw_dir / f"{safe_name(source_id)}.json"
                path.write_bytes(raw)
                self.records.append(
                    FetchRecord(
                        source_id=source_id,
                        method=method,
                        url=url,
                        fetched_at_utc=fetched_at,
                        status=status,
                        content_type=content_type,
                        byte_length=len(raw),
                        sha256=digest,
                        raw_path=str(path.relative_to(self.out_dir)),
                        error=None,
                    )
                )
                try:
                    return json.loads(raw.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    last_error = f"response is not valid UTF-8 JSON: {exc}"
                    self.records[-1].error = last_error
                    return None
            except urllib.error.HTTPError as exc:
                body_preview = exc.read(4096).decode("utf-8", errors="replace")
                last_error = f"HTTP {exc.code}: {body_preview[:1000]}"
                retry_after = exc.headers.get("Retry-After")
                if exc.code in {429, 500, 502, 503, 504} and attempt < self.retries:
                    delay = float(retry_after) if retry_after and retry_after.isdigit() else 2**attempt
                    time.sleep(min(delay, 15))
                    continue
                self.records.append(
                    FetchRecord(
                        source_id=source_id,
                        method=method,
                        url=url,
                        fetched_at_utc=fetched_at,
                        status=exc.code,
                        content_type=exc.headers.get("Content-Type"),
                        byte_length=len(body_preview.encode("utf-8")),
                        sha256=None,
                        raw_path=None,
                        error=last_error,
                    )
                )
                return None
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_error = f"{type(exc).__name__}: {exc}"
                if attempt < self.retries:
                    time.sleep(2**attempt)
                    continue
                self.records.append(
                    FetchRecord(
                        source_id=source_id,
                        method=method,
                        url=url,
                        fetched_at_utc=fetched_at,
                        status=None,
                        content_type=None,
                        byte_length=0,
                        sha256=None,
                        raw_path=None,
                        error=last_error,
                    )
                )
                return None
        return None


def btc_value_to_btc(value_sats: int | float | None) -> float:
    return float(value_sats or 0) / 100_000_000.0


def get_prevout_address(vin: dict[str, Any]) -> str | None:
    prevout = vin.get("prevout")
    if not isinstance(prevout, dict):
        return None
    addr = prevout.get("scriptpubkey_address")
    return str(addr) if addr else None


def get_prevout_value(vin: dict[str, Any]) -> int:
    prevout = vin.get("prevout")
    if not isinstance(prevout, dict):
        return 0
    return int(prevout.get("value") or 0)


def get_vout_address(vout: dict[str, Any]) -> str | None:
    addr = vout.get("scriptpubkey_address")
    return str(addr) if addr else None


def get_vout_value(vout: dict[str, Any]) -> int:
    return int(vout.get("value") or 0)


def collect_btc_mempool_pages(
    collector: Collector, address: str, expected_tx_count: int | None
) -> list[dict[str, Any]]:
    txs: list[dict[str, Any]] = []
    after_txid: str | None = None
    max_pages = 400
    for page in range(max_pages):
        base = f"https://mempool.space/api/address/{address}/txs/chain"
        url = base if not after_txid else f"{base}/{urllib.parse.quote(after_txid)}"
        data = collector.request_json(f"btc_mempool_txs_page_{page:04d}", url)
        if not isinstance(data, list) or not data:
            break
        new_items = [item for item in data if isinstance(item, dict)]
        txs.extend(new_items)
        after_txid = str(new_items[-1].get("txid") or "") if new_items else None
        if not after_txid:
            break
        if expected_tx_count is not None and len(txs) >= expected_tx_count:
            break
        if len(new_items) < 25:
            break
        time.sleep(0.15)
    dedup: dict[str, dict[str, Any]] = {}
    for tx in txs:
        txid = str(tx.get("txid") or "")
        if txid:
            dedup[txid] = tx
    return list(dedup.values())


def summarize_btc(
    address: str,
    mempool_stats: dict[str, Any] | None,
    txs: list[dict[str, Any]],
    utxos: list[dict[str, Any]] | None,
    backup_sources: dict[str, Any],
) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    counterparties_in: collections.Counter[str] = collections.Counter()
    counterparties_out: collections.Counter[str] = collections.Counter()
    coinput_addresses: collections.Counter[str] = collections.Counter()
    output_fanouts: list[int] = []
    input_fanins: list[int] = []
    round_output_count = 0
    total_relevant_outputs = 0

    for tx in txs:
        vin = tx.get("vin") if isinstance(tx.get("vin"), list) else []
        vout = tx.get("vout") if isinstance(tx.get("vout"), list) else []
        target_input = sum(
            get_prevout_value(i) for i in vin if get_prevout_address(i) == address
        )
        target_output = sum(
            get_vout_value(o) for o in vout if get_vout_address(o) == address
        )
        if target_input == 0 and target_output == 0:
            continue

        ts = None
        status = tx.get("status")
        if isinstance(status, dict) and status.get("block_time") is not None:
            ts = int(status["block_time"])

        direction = (
            "mixed"
            if target_input and target_output
            else "outgoing"
            if target_input
            else "incoming"
        )
        all_input_addresses = {
            a for a in (get_prevout_address(i) for i in vin) if a and a != address
        }
        all_output_addresses = {
            a for a in (get_vout_address(o) for o in vout) if a and a != address
        }

        if target_output:
            for cp in all_input_addresses:
                counterparties_in[cp] += 1
        if target_input:
            for cp in all_output_addresses:
                counterparties_out[cp] += 1
            for cp in all_input_addresses:
                coinput_addresses[cp] += 1

        output_fanouts.append(len(vout))
        input_fanins.append(len(vin))
        for out in vout:
            val = get_vout_value(out)
            if val > 0:
                total_relevant_outputs += 1
                if val % 100_000 == 0 or val % 1_000_000 == 0:
                    round_output_count += 1

        events.append(
            {
                "txid": tx.get("txid"),
                "timestamp_unix": ts,
                "timestamp_utc": (
                    dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc)
                    .replace(microsecond=0)
                    .isoformat()
                    if ts
                    else None
                ),
                "direction": direction,
                "gross_received_sats": target_output,
                "gross_spent_sats": target_input,
                "net_sats": target_output - target_input,
                "input_count": len(vin),
                "output_count": len(vout),
                "other_input_address_count": len(all_input_addresses),
                "other_output_address_count": len(all_output_addresses),
                "fee_sats": int(tx.get("fee") or 0),
                "size": tx.get("size"),
                "weight": tx.get("weight"),
            }
        )

    events.sort(key=lambda item: (item["timestamp_unix"] is None, item["timestamp_unix"] or 0))
    received_events = [e for e in events if e["gross_received_sats"] > 0]
    spent_events = [e for e in events if e["gross_spent_sats"] > 0]

    chain = (mempool_stats or {}).get("chain_stats") or {}
    mempool = (mempool_stats or {}).get("mempool_stats") or {}
    funded = int(chain.get("funded_txo_sum") or 0)
    spent = int(chain.get("spent_txo_sum") or 0)
    pending_funded = int(mempool.get("funded_txo_sum") or 0)
    pending_spent = int(mempool.get("spent_txo_sum") or 0)

    def top(counter: collections.Counter[str], n: int = 30) -> list[dict[str, Any]]:
        return [{"address": k, "transaction_mentions": v} for k, v in counter.most_common(n)]

    return {
        "address": address,
        "network": "Bitcoin mainnet",
        "address_type": "legacy P2PKH (Base58 prefix 1)",
        "primary_source_available": isinstance(mempool_stats, dict),
        "chain_stats": {
            "tx_count": int(chain.get("tx_count") or len(events)),
            "funded_txo_count": int(chain.get("funded_txo_count") or 0),
            "funded_txo_sum_sats": funded,
            "funded_txo_sum_btc": btc_value_to_btc(funded),
            "spent_txo_count": int(chain.get("spent_txo_count") or 0),
            "spent_txo_sum_sats": spent,
            "spent_txo_sum_btc": btc_value_to_btc(spent),
            "confirmed_balance_sats": funded - spent,
            "confirmed_balance_btc": btc_value_to_btc(funded - spent),
            "pending_balance_sats": pending_funded - pending_spent,
            "pending_balance_btc": btc_value_to_btc(pending_funded - pending_spent),
        },
        "transaction_analysis": {
            "transactions_retrieved": len(events),
            "incoming_or_mixed_tx_count": len(received_events),
            "outgoing_or_mixed_tx_count": len(spent_events),
            "mixed_tx_count": sum(1 for e in events if e["direction"] == "mixed"),
            "first_seen_utc": events[0]["timestamp_utc"] if events else None,
            "last_seen_utc": events[-1]["timestamp_utc"] if events else None,
            "largest_gross_receive_btc": (
                btc_value_to_btc(max(e["gross_received_sats"] for e in received_events))
                if received_events
                else 0
            ),
            "largest_gross_spend_btc": (
                btc_value_to_btc(max(e["gross_spent_sats"] for e in spent_events))
                if spent_events
                else 0
            ),
            "median_gross_receive_btc": (
                btc_value_to_btc(
                    int(statistics.median(e["gross_received_sats"] for e in received_events))
                )
                if received_events
                else 0
            ),
            "median_output_count": statistics.median(output_fanouts) if output_fanouts else 0,
            "max_output_count": max(output_fanouts) if output_fanouts else 0,
            "median_input_count": statistics.median(input_fanins) if input_fanins else 0,
            "max_input_count": max(input_fanins) if input_fanins else 0,
            "round_output_ratio_weak_feature": (
                round_output_count / total_relevant_outputs if total_relevant_outputs else None
            ),
        },
        "utxo_analysis": {
            "utxo_count": len(utxos) if isinstance(utxos, list) else None,
            "utxo_sum_sats": (
                sum(int(u.get("value") or 0) for u in utxos)
                if isinstance(utxos, list)
                else None
            ),
        },
        "top_counterparties_incoming_context": top(counterparties_in),
        "top_counterparties_outgoing_context": top(counterparties_out),
        "coinput_candidates": top(coinput_addresses),
        "events": events,
        "backup_sources": backup_sources,
        "interpretation_caveats": [
            "A Bitcoin address is not equivalent to a wallet, person, or organization.",
            "Other addresses in a transaction are transaction counterparties, not automatically the beneficial counterparty.",
            "Common-input clustering is a heuristic and may fail for CoinJoin, PayJoin, shared custody, or collaborative transactions.",
            "Change-output identification is heuristic; this probe does not declare a change address without corroboration.",
            "Total received is address reuse volume, not profit, wealth, or current holdings.",
        ],
    }


def normalize_trongrid_trc20_item(item: dict[str, Any], target: str) -> dict[str, Any]:
    token = item.get("token_info") if isinstance(item.get("token_info"), dict) else {}
    decimals = int(token.get("decimals") or 0)
    raw_value = str(item.get("value") or "0")
    try:
        value_int = int(raw_value)
    except ValueError:
        value_int = 0
    amount = value_int / (10**decimals) if decimals >= 0 else float(value_int)
    sender = str(item.get("from") or "")
    recipient = str(item.get("to") or "")
    ts_ms = int(item.get("block_timestamp") or 0)
    return {
        "txid": item.get("transaction_id"),
        "block_timestamp_ms": ts_ms,
        "timestamp_utc": (
            dt.datetime.fromtimestamp(ts_ms / 1000, tz=dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            if ts_ms
            else None
        ),
        "from": sender,
        "to": recipient,
        "direction": "incoming" if recipient == target else "outgoing" if sender == target else "other",
        "contract_address": token.get("address"),
        "token_symbol": token.get("symbol"),
        "token_name": token.get("name"),
        "decimals": decimals,
        "raw_value": raw_value,
        "amount": amount,
        "type": item.get("type"),
    }


def collect_trongrid_paginated(
    collector: Collector, address: str, endpoint_suffix: str, source_prefix: str
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    fingerprint: str | None = None
    for page in range(100):
        params = {"only_confirmed": "true", "limit": "200", "order_by": "block_timestamp,asc"}
        if fingerprint:
            params["fingerprint"] = fingerprint
        url = (
            f"https://api.trongrid.io/v1/accounts/{address}/{endpoint_suffix}?"
            + urllib.parse.urlencode(params)
        )
        data = collector.request_json(f"{source_prefix}_page_{page:04d}", url)
        if not isinstance(data, dict):
            break
        page_data = data.get("data")
        if not isinstance(page_data, list):
            break
        items.extend(x for x in page_data if isinstance(x, dict))
        meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
        fingerprint_new = meta.get("fingerprint")
        if not page_data or not fingerprint_new or fingerprint_new == fingerprint:
            break
        fingerprint = str(fingerprint_new)
        time.sleep(0.15)
    dedup: dict[tuple[Any, ...], dict[str, Any]] = {}
    for item in items:
        key = (
            item.get("transaction_id") or item.get("txID"),
            item.get("block_timestamp"),
            item.get("from"),
            item.get("to"),
            item.get("value"),
            (item.get("token_info") or {}).get("address")
            if isinstance(item.get("token_info"), dict)
            else None,
        )
        dedup[key] = item
    return list(dedup.values())


def summarize_tron(
    address: str,
    account_data: dict[str, Any] | None,
    fullnode_account: dict[str, Any] | None,
    trc20_raw: list[dict[str, Any]],
    trx_raw: list[dict[str, Any]],
    tronscan_data: dict[str, Any],
) -> dict[str, Any]:
    transfers = [normalize_trongrid_trc20_item(x, address) for x in trc20_raw]
    transfers = [x for x in transfers if x["direction"] in {"incoming", "outgoing"}]
    transfers.sort(key=lambda x: x["block_timestamp_ms"])

    verified_usdt = [
        x for x in transfers if str(x.get("contract_address") or "") == TRON_USDT_CONTRACT
    ]
    incoming_usdt = [x for x in verified_usdt if x["direction"] == "incoming"]
    outgoing_usdt = [x for x in verified_usdt if x["direction"] == "outgoing"]
    incoming_counterparties: collections.Counter[str] = collections.Counter(
        x["from"] for x in incoming_usdt
    )
    outgoing_counterparties: collections.Counter[str] = collections.Counter(
        x["to"] for x in outgoing_usdt
    )

    token_contracts = collections.Counter(str(x.get("contract_address") or "") for x in transfers)
    suspicious_small = [
        x
        for x in transfers
        if x.get("amount") is not None
        and abs(float(x["amount"])) < 0.0001
        and x.get("contract_address") != TRON_USDT_CONTRACT
    ]
    round_usdt = [
        x
        for x in verified_usdt
        if float(x["amount"]).is_integer() and int(float(x["amount"])) % 100 == 0
    ]

    account_obj: dict[str, Any] = {}
    if isinstance(account_data, dict):
        data = account_data.get("data")
        if isinstance(data, list) and data and isinstance(data[0], dict):
            account_obj = data[0]
    if not account_obj and isinstance(fullnode_account, dict):
        account_obj = fullnode_account

    balance_sun = int(account_obj.get("balance") or 0) if account_obj else 0
    create_time = int(account_obj.get("create_time") or 0) if account_obj else 0
    latest_op = int(
        account_obj.get("latest_opration_time")
        or account_obj.get("latest_operation_time")
        or 0
    ) if account_obj else 0

    def cp_list(counter: collections.Counter[str]) -> list[dict[str, Any]]:
        return [{"address": addr, "transfer_count": count} for addr, count in counter.most_common(50)]

    first_ts = transfers[0]["timestamp_utc"] if transfers else None
    last_ts = transfers[-1]["timestamp_utc"] if transfers else None

    return {
        "address": address,
        "network": "TRON mainnet",
        "hex_address": "41da383c182b70b7d6c91487a4e5fb44d415fbec56",
        "account_state": {
            "account_found": bool(account_obj),
            "trx_balance_sun": balance_sun,
            "trx_balance": balance_sun / 1_000_000,
            "create_time_utc": (
                dt.datetime.fromtimestamp(create_time / 1000, tz=dt.timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                if create_time
                else None
            ),
            "latest_operation_time_utc": (
                dt.datetime.fromtimestamp(latest_op / 1000, tz=dt.timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                if latest_op
                else None
            ),
            "account_name_hex": account_obj.get("account_name") if account_obj else None,
            "account_type": account_obj.get("type") if account_obj else None,
            "owner_permission": account_obj.get("owner_permission") if account_obj else None,
            "active_permission": account_obj.get("active_permission") if account_obj else None,
        },
        "trc20_analysis": {
            "all_trc20_events_retrieved": len(transfers),
            "distinct_token_contracts": len([x for x in token_contracts if x]),
            "verified_usdt_event_count": len(verified_usdt),
            "verified_usdt_incoming_count": len(incoming_usdt),
            "verified_usdt_outgoing_count": len(outgoing_usdt),
            "verified_usdt_total_in": sum(float(x["amount"]) for x in incoming_usdt),
            "verified_usdt_total_out": sum(float(x["amount"]) for x in outgoing_usdt),
            "verified_usdt_net_flow": sum(float(x["amount"]) for x in incoming_usdt)
            - sum(float(x["amount"]) for x in outgoing_usdt),
            "largest_usdt_in": max((float(x["amount"]) for x in incoming_usdt), default=0),
            "largest_usdt_out": max((float(x["amount"]) for x in outgoing_usdt), default=0),
            "first_trc20_seen_utc": first_ts,
            "last_trc20_seen_utc": last_ts,
            "round_usdt_event_ratio_weak_feature": (
                len(round_usdt) / len(verified_usdt) if verified_usdt else None
            ),
            "small_non_usdt_event_count_possible_spam": len(suspicious_small),
        },
        "top_usdt_incoming_counterparties": cp_list(incoming_counterparties),
        "top_usdt_outgoing_counterparties": cp_list(outgoing_counterparties),
        "verified_usdt_transfers": verified_usdt,
        "other_trc20_transfers": [
            x for x in transfers if x.get("contract_address") != TRON_USDT_CONTRACT
        ],
        "trx_transaction_count_retrieved": len(trx_raw),
        "tronscan_backup": tronscan_data,
        "interpretation_caveats": [
            "A TRON address can be a platform-controlled deposit address whose economic beneficiary is a customer.",
            "TRC-20 history can contain spam, fake-token, zero-value, and dust events; only the official USDT contract is aggregated as USDT.",
            "Incoming and outgoing counterparties are not identities unless independently labelled.",
            "A large round transfer is a behavioral feature, not proof of exchange, OTC, laundering, or criminal activity.",
            "Current token balance should be derived from current state or reconciled history, not inferred from one observed transfer.",
        ],
    }


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def format_num(value: Any) -> str:
    if value is None:
        return "not established"
    if isinstance(value, float):
        return f"{value:,.8f}".rstrip("0").rstrip(".")
    return str(value)


def build_markdown(summary: dict[str, Any]) -> str:
    btc = summary["bitcoin"]
    tron = summary["tron"]
    bstats = btc["chain_stats"]
    tstats = tron["trc20_analysis"]
    lines = [
        "# Public on-chain probe — reproducible acquisition summary",
        "",
        f"- Collected at: `{summary['generated_at_utc']}`",
        f"- BTC address: `{btc['address']}`",
        f"- TRON address: `{tron['address']}`",
        "",
        "## Bitcoin",
        "",
        f"- Primary mempool.space data available: **{btc['primary_source_available']}**",
        f"- Confirmed transactions: **{bstats['tx_count']}**",
        f"- Total funded outputs: **{format_num(bstats['funded_txo_sum_btc'])} BTC**",
        f"- Total spent outputs: **{format_num(bstats['spent_txo_sum_btc'])} BTC**",
        f"- Confirmed address balance: **{format_num(bstats['confirmed_balance_btc'])} BTC**",
        f"- First seen: **{btc['transaction_analysis']['first_seen_utc']}**",
        f"- Last seen: **{btc['transaction_analysis']['last_seen_utc']}**",
        f"- Retrieved transactions: **{btc['transaction_analysis']['transactions_retrieved']}**",
        "",
        "## TRON",
        "",
        f"- Account state available: **{tron['account_state']['account_found']}**",
        f"- TRX balance: **{format_num(tron['account_state']['trx_balance'])} TRX**",
        f"- TRC-20 events retrieved: **{tstats['all_trc20_events_retrieved']}**",
        f"- Verified USDT incoming: **{format_num(tstats['verified_usdt_total_in'])} USDT** "
        f"({tstats['verified_usdt_incoming_count']} events)",
        f"- Verified USDT outgoing: **{format_num(tstats['verified_usdt_total_out'])} USDT** "
        f"({tstats['verified_usdt_outgoing_count']} events)",
        f"- Verified USDT net flow: **{format_num(tstats['verified_usdt_net_flow'])} USDT**",
        f"- First TRC-20 seen: **{tstats['first_trc20_seen_utc']}**",
        f"- Last TRC-20 seen: **{tstats['last_trc20_seen_utc']}**",
        "",
        "## Evidence-control notes",
        "",
        "- Raw responses are preserved under `raw/` with URL, timestamp, status, byte length and SHA-256 in `manifest.json`.",
        "- No address is attributed to a person or organization solely from on-chain behavior.",
        "- Source failures remain visible in the manifest.",
        "- This run is read-only and does not use credentials or non-public data.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="out", help="Output directory")
    args = parser.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    collector = Collector(out_dir)

    btc_stats = collector.request_json(
        "btc_mempool_address", f"https://mempool.space/api/address/{BTC_ADDRESS}"
    )
    expected = None
    if isinstance(btc_stats, dict):
        chain = btc_stats.get("chain_stats")
        if isinstance(chain, dict):
            expected = int(chain.get("tx_count") or 0)
    btc_txs = collect_btc_mempool_pages(collector, BTC_ADDRESS, expected)
    btc_utxos = collector.request_json(
        "btc_mempool_utxo", f"https://mempool.space/api/address/{BTC_ADDRESS}/utxo"
    )
    btc_backups = {
        "blockstream_address": collector.request_json(
            "btc_blockstream_address", f"https://blockstream.info/api/address/{BTC_ADDRESS}"
        ),
        "blockcypher_address": collector.request_json(
            "btc_blockcypher_address",
            f"https://api.blockcypher.com/v1/btc/main/addrs/{BTC_ADDRESS}?limit=200",
        ),
        "blockchain_info_rawaddr": collector.request_json(
            "btc_blockchain_info_rawaddr",
            f"https://blockchain.info/rawaddr/{BTC_ADDRESS}?limit=50",
        ),
    }
    btc_summary = summarize_btc(
        BTC_ADDRESS,
        btc_stats if isinstance(btc_stats, dict) else None,
        btc_txs,
        btc_utxos if isinstance(btc_utxos, list) else None,
        btc_backups,
    )

    tron_account = collector.request_json(
        "tron_trongrid_account",
        f"https://api.trongrid.io/v1/accounts/{TRON_ADDRESS}?only_confirmed=true",
    )
    tron_fullnode = collector.request_json(
        "tron_fullnode_getaccount",
        "https://api.trongrid.io/wallet/getaccount",
        method="POST",
        body={"address": TRON_ADDRESS, "visible": True},
    )
    tron_resource = collector.request_json(
        "tron_fullnode_getaccountresource",
        "https://api.trongrid.io/wallet/getaccountresource",
        method="POST",
        body={"address": TRON_ADDRESS, "visible": True},
    )
    tron_trc20 = collect_trongrid_paginated(
        collector, TRON_ADDRESS, "transactions/trc20", "tron_trongrid_trc20"
    )
    tron_txs = collect_trongrid_paginated(
        collector, TRON_ADDRESS, "transactions", "tron_trongrid_transactions"
    )
    encoded_addr = urllib.parse.quote(TRON_ADDRESS)
    tronscan_backups = {
        "accountv2": collector.request_json(
            "tron_tronscan_accountv2",
            f"https://apilist.tronscanapi.com/api/accountv2?address={encoded_addr}",
        ),
        "account": collector.request_json(
            "tron_tronscan_account",
            f"https://apilist.tronscanapi.com/api/account?address={encoded_addr}",
        ),
        "trc20_transfers": collector.request_json(
            "tron_tronscan_trc20_transfers",
            "https://apilist.tronscanapi.com/api/token_trc20/transfers?"
            + urllib.parse.urlencode(
                {
                    "limit": 200,
                    "start": 0,
                    "sort": "-timestamp",
                    "count": "true",
                    "relatedAddress": TRON_ADDRESS,
                }
            ),
        ),
        "account_resource": tron_resource,
    }
    tron_summary = summarize_tron(
        TRON_ADDRESS,
        tron_account if isinstance(tron_account, dict) else None,
        tron_fullnode if isinstance(tron_fullnode, dict) else None,
        tron_trc20,
        tron_txs,
        tronscan_backups,
    )

    summary = {
        "schema_version": "onchain-probe-v0.1",
        "generated_at_utc": utcnow(),
        "bitcoin": btc_summary,
        "tron": tron_summary,
    }

    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    (out_dir / "summary.md").write_text(build_markdown(summary), encoding="utf-8")
    (out_dir / "manifest.json").write_text(
        json.dumps([asdict(r) for r in collector.records], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    write_csv(
        out_dir / "btc_events.csv",
        btc_summary["events"],
        [
            "txid",
            "timestamp_utc",
            "direction",
            "gross_received_sats",
            "gross_spent_sats",
            "net_sats",
            "input_count",
            "output_count",
            "other_input_address_count",
            "other_output_address_count",
            "fee_sats",
            "size",
            "weight",
        ],
    )
    write_csv(
        out_dir / "tron_verified_usdt.csv",
        tron_summary["verified_usdt_transfers"],
        [
            "txid",
            "timestamp_utc",
            "from",
            "to",
            "direction",
            "contract_address",
            "token_symbol",
            "raw_value",
            "amount",
        ],
    )

    print((out_dir / "summary.md").read_text(encoding="utf-8"))
    print("MANIFEST")
    for record in collector.records:
        print(
            json.dumps(
                {
                    "source_id": record.source_id,
                    "status": record.status,
                    "bytes": record.byte_length,
                    "sha256": record.sha256,
                    "error": record.error,
                },
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
