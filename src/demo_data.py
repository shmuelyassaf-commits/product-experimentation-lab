"""Generate clearly labelled synthetic data for a reproducible walkthrough."""

from __future__ import annotations

import numpy as np
import pandas as pd


def make_demo_data(users: int = 10000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    version = rng.choice(["gate_30", "gate_40"], size=users)
    is_treatment = version == "gate_40"
    retention_1 = rng.binomial(1, 0.445 - is_treatment * 0.002)
    retention_7 = rng.binomial(1, 0.188 - is_treatment * 0.008)
    rounds = rng.lognormal(mean=4.0 - is_treatment * 0.015, sigma=1.1, size=users).round().astype(int)
    return pd.DataFrame(
        {
            "userid": np.arange(1, users + 1),
            "version": version,
            "sum_gamerounds": rounds,
            "retention_1": retention_1.astype(bool),
            "retention_7": retention_7.astype(bool),
        }
    )

