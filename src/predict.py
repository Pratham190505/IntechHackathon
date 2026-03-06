from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from explanation_generator import generate_explanation


def _load_container_ids(repo_root: Path, n: int) -> pd.Series:
    path = repo_root / "data" / "container_ids.csv"
    if path.exists():
        ids_df = pd.read_csv(path)
        # Accept either a single-column CSV or one with 'Container_ID'
        if "Container_ID" in ids_df.columns:
            series = ids_df["Container_ID"]
        else:
            series = ids_df.iloc[:, 0]
        if len(series) >= n:
            return series.iloc[:n].reset_index(drop=True)
        # pad if short
        padded = list(series.astype(str)) + [f"GEN-{i}" for i in range(len(series), n)]
        return pd.Series(padded)

    return pd.Series([f"GEN-{i}" for i in range(n)])


def predict(
    processed_realtime_csv: Path,
    risk_model_path: Path,
    anomaly_model_path: Path,
    out_csv: Path,
) -> None:
    repo_root = Path(__file__).resolve().parents[1]

    df_rt = pd.read_csv(processed_realtime_csv)
    df_features = df_rt.copy()

    # Anomaly (computed from features only)
    iso_model = joblib.load(anomaly_model_path)
    anomaly_predictions = iso_model.predict(df_features)
    anomaly_flag = (anomaly_predictions == -1).astype(int)
    df_rt["Anomaly_Flag"] = anomaly_flag

    # Risk model (must use the same feature columns it was trained on)
    risk_model = joblib.load(risk_model_path)
    risk_prob = risk_model.predict_proba(df_features)[:, 1]
    risk_score = np.clip(risk_prob * 100, 0, 100)

    # Bump risk for anomalies
    risk_score = np.clip(risk_score + (anomaly_flag * 20), 0, 100)

    df_rt["Risk_Score"] = risk_score
    df_rt["Risk_Level"] = np.where(df_rt["Risk_Score"] > 70, "Critical", "Low")

    df_rt["Explanation"] = df_rt.apply(generate_explanation, axis=1)

    container_ids = _load_container_ids(repo_root, len(df_rt))
    output_df = pd.DataFrame(
        {
            "Container_ID": container_ids,
            "Risk_Score": pd.Series(df_rt["Risk_Score"]).round(2),
            "Risk_Level": df_rt["Risk_Level"],
            "Explanation": df_rt["Explanation"],
        }
    )

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(out_csv, index=False)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description="Generate container risk predictions.")
    parser.add_argument(
        "--data",
        type=Path,
        default=repo_root / "processed" / "processed_realtime_data.csv",
    )
    parser.add_argument(
        "--risk-model",
        type=Path,
        default=repo_root / "models" / "risk_model.pkl",
    )
    parser.add_argument(
        "--anomaly-model",
        type=Path,
        default=repo_root / "models" / "anomaly_model.pkl",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=repo_root / "outputs" / "container_risk_predictions.csv",
    )
    args = parser.parse_args()

    predict(args.data, args.risk_model, args.anomaly_model, args.out)


if __name__ == "__main__":
    main()
