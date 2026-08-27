# Product Experimentation Lab

A small A/B testing project based on the Cookie Cats mobile game dataset.

## Question

Should the product team move the first game gate from level 30 to level 40?

The main metric is Day-7 retention. Day-1 retention is a secondary metric, and game rounds are used as a guardrail.

## What I did

- Checked the data for missing values, duplicates, and an unbalanced split between groups.
- Compared retention between control and treatment groups.
- Used confidence intervals and statistical tests to check whether the difference was reliable.
- Checked that the change did not create a clear negative effect on engagement.
- Wrote a simple recommendation: roll out, do not roll out, or run another test.

## Tools

Python · pandas · SQL · Streamlit · unit tests

## Run the project

```bash
pip install -r requirements.txt
python -m src.run_analysis --demo
streamlit run app/app.py
```

## Data

The project can run with the public Cookie Cats dataset from Kaggle. The repository does not include the original file.

It also includes a simulated demo dataset, so the analysis can be run without downloading data. Demo results are clearly marked and are not presented as results from the original experiment.
