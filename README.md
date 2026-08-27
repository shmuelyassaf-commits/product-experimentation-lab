# Product Experimentation Lab

An end-to-end A/B-test analysis project that answers a product decision, not only a statistical question:

> Should a product team roll out a change if it changes user retention, but may affect engagement?

The project uses the public **Cookie Cats** experiment when the source CSV is supplied locally. The experiment randomly assigned players to a control or treatment version that moved the first game gate from level 30 to level 40. The analysis evaluates Day-1 and Day-7 retention as primary outcomes, with game rounds as a guardrail metric.

## Why this project is portfolio-ready

It demonstrates the work of a Product Data Analyst:

- turns a product question into hypotheses, metrics, and a decision rule;
- checks data quality and sample-ratio mismatch before interpreting results;
- runs two-proportion z-tests, confidence intervals, bootstrap analysis, and a practical-significance check;
- produces a decision memo rather than stopping at a p-value;
- includes SQL, Python, automated tests, and an optional Streamlit decision dashboard.

## Project question

**Change:** Move the first progression gate from level 30 (control) to level 40 (treatment).

**Primary metric:** Day-7 retention.

**Secondary metric:** Day-1 retention.

**Guardrail:** Total game rounds during the observation window.

**Decision rule:** Roll out only if the Day-7 retention effect is statistically significant, meets the practical threshold, and does not materially harm engagement.

## Data source

Download `cookie_cats.csv` from the [Cookie Cats Mobile Games A/B Testing dataset](https://www.kaggle.com/datasets/mursideyarkin/mobile-games-ab-testing-cookie-cats) and save it to:

```text
data/raw/cookie_cats.csv
```

The source data is intentionally not committed to this repository. For a quick, reproducible walkthrough without the source file, use `--demo` to generate a clearly labelled simulated dataset.

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Run against simulated demonstration data
python -m src.run_analysis --demo

# Run against the downloaded public source data
python -m src.run_analysis --input data/raw/cookie_cats.csv

# Launch the interactive decision dashboard
streamlit run app/app.py
```

## Repository structure

```text
app/                    Streamlit decision dashboard
data/raw/               Public source CSV goes here (gitignored)
data/processed/         Generated metrics (gitignored)
reports/                Generated figures and decision memo (gitignored)
sql/                    Reusable SQL for experiment metrics
src/                    Analysis, validation, and demo-data modules
tests/                  Automated validation tests
```

## Analysis workflow

1. Validate schema, duplicates, nulls, and treatment assignment.
2. Test sample-ratio mismatch (SRM).
3. Compare retention rates using a two-proportion z-test and 95% confidence intervals.
4. Bootstrap the engagement difference to handle a skewed distribution.
5. Evaluate practical significance, not only statistical significance.
6. Produce a recommendation: **roll out**, **do not roll out**, or **run a follow-up test**.

## Interview story

“I started with a product decision rather than a generic analysis. I checked whether the experiment was trustworthy, chose Day-7 retention as the primary metric, added engagement as a guardrail, quantified uncertainty, and wrote a recommendation that a product manager could act on.”

## Important limitation

This is an analysis of a historical A/B-test dataset. It does not claim that a before/after comparison alone proves causality. A pre/post view can be useful as context, but random assignment is the basis for the causal conclusion here.

