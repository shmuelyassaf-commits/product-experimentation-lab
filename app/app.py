"""Interactive A/B-test decision dashboard."""

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.demo_data import make_demo_data
from src.experiment import analyze

st.set_page_config(page_title="Experiment Decision Engine", layout="wide")
st.title("Experiment Decision Engine")
st.caption("A product decision dashboard for A/B-test results")

uploaded = st.file_uploader("Upload cookie_cats.csv (optional)", type="csv")
data = pd.read_csv(uploaded) if uploaded else make_demo_data()
results = analyze(data)

left, middle, right = st.columns(3)
left.metric("Users", f"{results['data_quality']['rows']:,}")
middle.metric("Day-7 lift", f"{results['retention_7']['absolute_lift']:.2%}")
right.metric("Day-7 p-value", f"{results['retention_7']['p_value']:.4f}")

st.subheader(results["decision"]["recommendation"])
st.write(results["decision"]["reason"])

st.subheader("Retention comparison")
retention = pd.DataFrame(
    {
        "metric": ["Day 1", "Day 7"],
        "control": [results["retention_1"]["control_rate"], results["retention_7"]["control_rate"]],
        "treatment": [results["retention_1"]["treatment_rate"], results["retention_7"]["treatment_rate"]],
    }
).set_index("metric")
st.bar_chart(retention)

st.subheader("Trust checks")
st.json({"sample_ratio_mismatch": results["sample_ratio_mismatch"], "data_quality": results["data_quality"]})

