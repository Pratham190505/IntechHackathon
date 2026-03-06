from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def train_model(processed_historical_csv: Path, out_model_path: Path) -> None:
    df = pd.read_csv(processed_historical_csv)
    if "Risk_Label" not in df.columns:
        raise ValueError("processed historical data must include Risk_Label")

    X = df.drop(columns=["Risk_Label"])
    y = df["Risk_Label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    out_model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_model_path)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(description="Train the container risk model.")
    parser.add_argument(
        "--data",
        type=Path,
        default=repo_root / "processed" / "processed_historical_data.csv",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=repo_root / "models" / "risk_model.pkl",
    )
    args = parser.parse_args()

    train_model(args.data, args.out)


if __name__ == "__main__":
    main()
