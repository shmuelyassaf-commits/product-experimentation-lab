"""Core validation and statistics for a two-group product experiment."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import erf, sqrt
from typing import Any

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {"userid", "version", "sum_gamerounds", "retention_1", "retention_7"}
CONTROL = "gate_30"
TREATMENT = "gate_40"


@dataclass
class ProportionTest:
    metric: str
    control_rate: float
    treatment_rate: float
    absolute_lift: float
    relative_lift: float
    z_score: float
    p_value: float
    ci_low: float
    ci_high: float


def normal_cdf(value: float) -> float:
    return (1 + erf(value / sqrt(2))) / 2


def validate_schema(data: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    unknown_versions = set(data["version"].dropna().unique()).difference({CONTROL, TREATMENT})
    if unknown_versions:
        raise ValueError(f"Unexpected experiment groups: {sorted(unknown_versions)}")


def data_quality_report(data: pd.DataFrame) -> dict[str, Any]:
    validate_schema(data)
    groups = data["version"].value_counts().to_dict()
    return {
        "rows": int(len(data)),
        "duplicate_user_ids": int(data["userid"].duplicated().sum()),
        "null_values": {key: int(value) for key, value in data.isna().sum().to_dict().items()},
        "group_counts": {key: int(value) for key, value in groups.items()},
    }


def sample_ratio_mismatch(data: pd.DataFrame) -> dict[str, float]:
    """Chi-square SRM test for a 50/50 split (df=1)."""
    counts = data["version"].value_counts()
    observed_control = counts.get(CONTROL, 0)
    observed_treatment = counts.get(TREATMENT, 0)
    total = observed_control + observed_treatment
    expected = total / 2
    chi_square = ((observed_control - expected) ** 2 + (observed_treatment - expected) ** 2) / expected
    # Survival function for chi-square with one degree of freedom.
    p_value = 1 - erf(sqrt(chi_square / 2))
    return {"chi_square": float(chi_square), "p_value": float(p_value)}


def proportion_test(data: pd.DataFrame, metric: str) -> ProportionTest:
    control = data.loc[data["version"] == CONTROL, metric].astype(int)
    treatment = data.loc[data["version"] == TREATMENT, metric].astype(int)
    p_control, p_treatment = control.mean(), treatment.mean()
    pooled = (control.sum() + treatment.sum()) / (len(control) + len(treatment))
    standard_error_pooled = sqrt(pooled * (1 - pooled) * (1 / len(control) + 1 / len(treatment)))
    z_score = (p_treatment - p_control) / standard_error_pooled
    p_value = 2 * (1 - normal_cdf(abs(z_score)))
    standard_error_unpooled = sqrt(
        p_control * (1 - p_control) / len(control) + p_treatment * (1 - p_treatment) / len(treatment)
    )
    difference = p_treatment - p_control
    return ProportionTest(
        metric=metric,
        control_rate=float(p_control),
        treatment_rate=float(p_treatment),
        absolute_lift=float(difference),
        relative_lift=float(difference / p_control) if p_control else float("nan"),
        z_score=float(z_score),
        p_value=float(p_value),
        ci_low=float(difference - 1.96 * standard_error_unpooled),
        ci_high=float(difference + 1.96 * standard_error_unpooled),
    )


def bootstrap_mean_difference(data: pd.DataFrame, metric: str, iterations: int = 3000, seed: int = 42) -> dict[str, float]:
    control = data.loc[data["version"] == CONTROL, metric].to_numpy()
    treatment = data.loc[data["version"] == TREATMENT, metric].to_numpy()
    rng = np.random.default_rng(seed)
    differences = np.empty(iterations)
    for index in range(iterations):
        control_sample = rng.choice(control, size=len(control), replace=True)
        treatment_sample = rng.choice(treatment, size=len(treatment), replace=True)
        differences[index] = treatment_sample.mean() - control_sample.mean()
    return {
        "control_mean": float(control.mean()),
        "treatment_mean": float(treatment.mean()),
        "mean_difference": float(treatment.mean() - control.mean()),
        "ci_low": float(np.quantile(differences, 0.025)),
        "ci_high": float(np.quantile(differences, 0.975)),
    }


def decision(retention_7: ProportionTest, engagement: dict[str, float], min_practical_lift: float = 0.002) -> dict[str, str]:
    engagement_harmed = engagement["ci_high"] < 0
    significant = retention_7.p_value < 0.05
    meaningful = retention_7.absolute_lift >= min_practical_lift
    if significant and meaningful and not engagement_harmed:
        recommendation = "ROLL OUT"
        reason = "Day-7 retention improved by a statistically and practically meaningful amount without a confirmed engagement decline."
    elif significant and retention_7.absolute_lift < 0:
        recommendation = "DO NOT ROLL OUT"
        reason = "The treatment significantly reduced Day-7 retention."
    else:
        recommendation = "RUN FOLLOW-UP TEST"
        reason = "The available evidence does not support a confident rollout decision."
    return {"recommendation": recommendation, "reason": reason}


def analyze(data: pd.DataFrame) -> dict[str, Any]:
    quality = data_quality_report(data)
    retention_1 = proportion_test(data, "retention_1")
    retention_7 = proportion_test(data, "retention_7")
    engagement = bootstrap_mean_difference(data, "sum_gamerounds")
    return {
        "data_quality": quality,
        "sample_ratio_mismatch": sample_ratio_mismatch(data),
        "retention_1": asdict(retention_1),
        "retention_7": asdict(retention_7),
        "engagement_guardrail": engagement,
        "decision": decision(retention_7, engagement),
    }

