from __future__ import annotations

from typing import Any, Mapping


def generate_explanation(row: Mapping[str, Any]) -> str:
    reasons: list[str] = []

    weight_diff = float(row.get("weight_diff", 0) or 0)
    value_per_weight = float(row.get("value_per_weight", 0) or 0)
    long_dwell = int(row.get("long_dwell", 0) or 0)
    anomaly_flag = int(row.get("Anomaly_Flag", 0) or 0)

    if weight_diff > 500:
        reasons.append("Large mismatch between declared and measured weight")

    if value_per_weight > 1000:
        reasons.append("Unusual value-to-weight ratio")

    if long_dwell == 1:
        reasons.append("Container stayed unusually long at port")

    if anomaly_flag == 1:
        reasons.append("Shipment pattern deviates from normal trade behavior")

    if not reasons:
        return "Shipment appears normal with no significant anomalies"

    return ", ".join(reasons)
