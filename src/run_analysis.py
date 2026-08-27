"""CLI entry point for the Product Experimentation Lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.demo_data import make_demo_data
from src.experiment import analyze


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the A/B-test analysis.")
    parser.add_argument("--input", type=Path, help="Path to cookie_cats.csv")
    parser.add_argument("--demo", action="store_true", help="Use simulated data for a reproducible walkthrough")
    args = parser.parse_args()
    if bool(args.input) == bool(args.demo):
        parser.error("Choose exactly one: --input PATH or --demo")

    data = make_demo_data() if args.demo else pd.read_csv(args.input)
    results = analyze(data)
    output = Path("reports")
    output.mkdir(exist_ok=True)
    result_path = output / "experiment_results.json"
    result_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"\nSaved results to {result_path}")


if __name__ == "__main__":
    main()

