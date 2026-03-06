from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest


def train_anomaly_model(processed_historical_csv: Path, out_model_path: Path) -> None:
    df = pd.read_csv(processed_historical_csv)
    X = df.drop(columns=["Risk_Label"], errors="ignore")

    model = IsolationForest(n_estimators=200, contamination=0.05, random_state=42)
    model.fit(X)

    out_model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_model_path)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description="Train the anomaly detection model.")
    parser.add_argument(
        "--data",
        type=Path,
        default=repo_root / "processed" / "processed_historical_data.csv",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=repo_root / "models" / "anomaly_model.pkl",
    )
    args = parser.parse_args()

    train_anomaly_model(args.data, args.out)


if __name__ == "__main__":
    main()
