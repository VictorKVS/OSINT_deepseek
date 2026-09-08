import pytest

from father_osint.crypto.bitcoin import (
    EvidenceConflict,
    TraceState,
    cross_check_address_stats,
    parse_wallet_explorer_service_rows,
    reconcile_service_flow,
    trace_next_hop,
)


def test_cross_check_address_stats_agrees_across_source_shapes():
    result = cross_check_address_stats(
        {
            "blockstream": {
                "chain_stats": {
                    "tx_count": 27,
                    "funded_txo_count": 18,
                    "funded_txo_sum": 9_119_321,
                    "spent_txo_count": 18,
                    "spent_txo_sum": 9_119_321,
                }
            },
            "blockchain_info": {
                "n_tx": 27,
                "total_received": 9_119_321,
                "total_sent": 9_119_321,
                "final_balance": 0,
            },
        }
    )
    assert result.tx_count == 27
    assert result.final_balance == 0


def test_cross_check_address_stats_rejects_conflict():
    with pytest.raises(EvidenceConflict, match="tx_count"):
        cross_check_address_stats(
            {
                "a": {"n_tx": 27, "total_received": 10, "total_sent": 10, "final_balance": 0},
                "b": {"n_tx": 28, "total_received": 10, "total_sent": 10, "final_balance": 0},
            }
        )


def test_wallet_explorer_parser_survives_nested_rows():
    txid = "a" * 64
    html = f'''
    <table>
      <tr class="sent"><td class="date">2016-05-18 01:03:31</td>
        <td><table><tr><td>SatoshiDice.com-original</td></tr></table></td>
        <td><a href="/txid/{txid}">tx</a></td>
        <td class="amount diff"><em>-0.02500000</em></td>
      </tr>
    </table>
    '''
    rows = parse_wallet_explorer_service_rows(html, "SatoshiDice.com-original")
    assert len(rows) == 1
    assert rows[0].direction == "sent"
    assert rows[0].txid == txid
    assert rows[0].wallet_net_btc == -0.025


def test_wallet_explorer_zero_result_is_failure_when_label_exists():
    html = "<html>SatoshiDice.com-original but malformed table</html>"
    with pytest.raises(EvidenceConflict, match="zero rows"):
        parse_wallet_explorer_service_rows(html, "SatoshiDice.com-original")


def test_exceptional_satoshidice_tx_keeps_service_and_other_flow_separate():
    wallet = {"1LJ3aPB1ru68xuqVbY8XzHK89HN7Z7j1Zz"}
    tx = {
        "fee": 6096,
        "vin": [
            {
                "prevout": {
                    "scriptpubkey_address": "1LJ3aPB1ru68xuqVbY8XzHK89HN7Z7j1Zz",
                    "value": 22_408_304,
                }
            }
        ],
        "vout": [
            {"scriptpubkey_address": "1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp", "value": 2_000_000},
            {"scriptpubkey_address": "1A1GUw9yWbBBVSCcAEux7vV4Ft3KxN7NzL", "value": 20_402_208},
        ],
    }
    flow = reconcile_service_flow(
        tx,
        wallet_addresses=wallet,
        is_service_address=lambda address: address.startswith("1dice"),
    )
    assert flow.wallet_delta_sat == -22_408_304
    assert flow.direct_service_outflow_sat == 2_000_000
    assert flow.other_external_outflow_sat == 20_402_208
    assert flow.mixed_destination is True
    assert flow.direct_service_outflow_sat != abs(flow.wallet_delta_sat)


def test_service_only_received_transaction_verifies_inflow():
    wallet = {"1TargetWalletAddress1111111111111111"}
    service = "1diceServiceAddress11111111111111111"
    tx = {
        "fee": 1000,
        "vin": [{"prevout": {"scriptpubkey_address": service, "value": 5_000_000}}],
        "vout": [
            {"scriptpubkey_address": "1TargetWalletAddress1111111111111111", "value": 1_900_000},
            {"scriptpubkey_address": "1ServiceChange111111111111111111111", "value": 3_099_000},
        ],
    }
    flow = reconcile_service_flow(
        tx,
        wallet_addresses=wallet,
        is_service_address=lambda _address: False,
        external_input_is_service=lambda address: address == service,
    )
    assert flow.verified_service_inflow_sat == 1_900_000
    assert flow.mixed_source is False


def test_trace_confidence_degrades_after_unrelated_input():
    state = TraceState(tracked_sat=10_000_000)
    clean = trace_next_hop(state, forwarded_sat=9_000_000)
    assert clean.confidence == 1.0
    assert clean.contaminated is False

    mixed = trace_next_hop(clean, forwarded_sat=8_000_000, unrelated_input_sat=9_000_000)
    assert mixed.contaminated is True
    assert 0 < mixed.confidence < 0.5


def test_trace_stop_condition_is_explicit():
    state = TraceState(tracked_sat=10_000_000)
    stopped = trace_next_hop(state, forwarded_sat=9_000_000, repeated_behavior_reached=True)
    assert stopped.stop_reason == "repeated_behavior"
