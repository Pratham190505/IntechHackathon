from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def _encode_series(series: pd.Series) -> pd.Series:
    # Factorize to integer codes; stable for a single run.
    codes, _ = pd.factorize(series.astype(str), sort=True)
    return pd.Series(codes, index=series.index)


def preprocess_historical(raw_csv: Path, out_csv: Path) -> None:
    df = pd.read_csv(raw_csv)

    # Basic missing handling
    df = df.fillna(0)

    # Time features
    df["Declaration_Date (YYYY-MM-DD)"] = pd.to_datetime(
        df["Declaration_Date (YYYY-MM-DD)"], errors="coerce"
    )
    df["Declaration_Time"] = pd.to_datetime(df["Declaration_Time"], errors="coerce")

    df["month"] = df["Declaration_Date (YYYY-MM-DD)"].dt.month.fillna(0).astype(int)
    df["day"] = df["Declaration_Date (YYYY-MM-DD)"].dt.day.fillna(0).astype(int)
    df["weekday"] = df["Declaration_Date (YYYY-MM-DD)"].dt.weekday.fillna(0).astype(int)
    df["hour"] = df["Declaration_Time"].dt.hour.fillna(0).astype(int)

    # Derived numeric features
    df["weight_diff"] = df["Measured_Weight"] - df["Declared_Weight"]
    df["weight_ratio"] = (df["Measured_Weight"] / df["Declared_Weight"]).replace(
        [float("inf"), -float("inf")], 0
    )
    df["value_per_weight"] = (df["Declared_Value"] / df["Declared_Weight"]).replace(
        [float("inf"), -float("inf")], 0
    )
    df["long_dwell"] = (df["Dwell_Time_Hours"] > 48).astype(int)

    # Risk label
    df["Risk_Label"] = df["Clearance_Status"].apply(lambda x: 0 if x == "Clear" else 1)

    # Encode categoricals
    for col in [
        "Trade_Regime (Import / Export / Transit)",
        "Origin_Country",
        "Destination_Port",
        "Destination_Country",
        "Shipping_Line",
    ]:
        if col in df.columns:
            df[col] = _encode_series(df[col])

    # Drop high-cardinality IDs and raw date fields
    drop_cols = [
        "Container_ID",
        "Importer_ID",
        "Exporter_ID",
        "Declaration_Date (YYYY-MM-DD)",
        "Declaration_Time",
        "Clearance_Status",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)


def preprocess_realtime(raw_csv: Path, out_csv: Path) -> None:
    df = pd.read_csv(raw_csv)
    df = df.fillna(0)

    df["Declaration_Date (YYYY-MM-DD)"] = pd.to_datetime(
        df["Declaration_Date (YYYY-MM-DD)"], errors="coerce"
    )
    df["Declaration_Time"] = pd.to_datetime(df["Declaration_Time"], errors="coerce")

    df["month"] = df["Declaration_Date (YYYY-MM-DD)"].dt.month.fillna(0).astype(int)
    df["day"] = df["Declaration_Date (YYYY-MM-DD)"].dt.day.fillna(0).astype(int)
    df["weekday"] = df["Declaration_Date (YYYY-MM-DD)"].dt.weekday.fillna(0).astype(int)
    df["hour"] = df["Declaration_Time"].dt.hour.fillna(0).astype(int)

    df["weight_diff"] = df["Measured_Weight"] - df["Declared_Weight"]
    df["weight_ratio"] = (df["Measured_Weight"] / df["Declared_Weight"]).replace(
        [float("inf"), -float("inf")], 0
    )
    df["value_per_weight"] = (df["Declared_Value"] / df["Declared_Weight"]).replace(
        [float("inf"), -float("inf")], 0
    )
    df["long_dwell"] = (df["Dwell_Time_Hours"] > 48).astype(int)

    for col in [
        "Trade_Regime (Import / Export / Transit)",
        "Origin_Country",
        "Destination_Port",
        "Destination_Country",
        "Shipping_Line",
    ]:
        if col in df.columns:
            df[col] = _encode_series(df[col])

    drop_cols = [
        "Container_ID",
        "Importer_ID",
        "Exporter_ID",
        "Declaration_Date (YYYY-MM-DD)",
        "Declaration_Time",
        "Clearance_Status",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description="Preprocess raw CSVs into model-ready features.")
    parser.add_argument(
        "--historical-in",
        type=Path,
        default=repo_root / "data" / "Historical Data.csv",
    )
    parser.add_argument(
        "--realtime-in",
        type=Path,
        default=repo_root / "data" / "Real-Time Data.csv",
    )
    parser.add_argument(
        "--historical-out",
        type=Path,
        default=repo_root / "processed" / "processed_historical_data.csv",
    )
    parser.add_argument(
        "--realtime-out",
        type=Path,
        default=repo_root / "processed" / "processed_realtime_data.csv",
    )
    args = parser.parse_args()

    preprocess_historical(args.historical_in, args.historical_out)
    preprocess_realtime(args.realtime_in, args.realtime_out)


if __name__ == "__main__":
    main()
