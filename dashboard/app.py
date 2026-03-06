from __future__ import annotations

from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    predictions_csv = repo_root / "outputs" / "container_risk_predictions.csv"

    try:
        import pandas as pd  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"Missing dependency 'pandas': {exc}")

    try:
        import streamlit as st  # type: ignore

        st.set_page_config(page_title="SmartContainer Risk Dashboard", layout="wide")
        st.title("SmartContainer Risk Dashboard")

        if not predictions_csv.exists():
            st.warning(
                f"No predictions found at {predictions_csv}. Run src/predict.py first."
            )
            return

        df = pd.read_csv(predictions_csv)
        st.dataframe(df, use_container_width=True)

        if "Risk_Level" in df.columns:
            st.subheader("Risk Level Counts")
            st.bar_chart(df["Risk_Level"].value_counts())

    except ModuleNotFoundError:
        # Fallback: CLI output (no extra dependencies)
        if not predictions_csv.exists():
            raise SystemExit(
                f"No predictions found at {predictions_csv}. Run 'python src/predict.py' first."
            )

        df = pd.read_csv(predictions_csv)
        print(df.head(20).to_string(index=False))
        print("\nTip: install Streamlit for a UI: pip install streamlit")


if __name__ == "__main__":
    main()
