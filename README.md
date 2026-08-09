# vahan-lead-source-cohort-analysis
Data analytics &amp; machine learning case study analyzing lead-source performance, FT conversion, SQL aggregation, and predictive factors using Python and Random Forest.

# Vahan Case Study — Lead-Source Cohort Performance

Solution to the Vahan case study on cohort (lead-source) performance: identifying the best-converting
lead sources, aggregating candidate-level data via SQL, and building a predictive model of FT
(full-time hire) conversion.

📄 **Full write-up:** [`Vahan_Case_Study_Assessment.pdf`](./Vahan_Case_Study_Assessment.pdf) — start here.

---

## Problem

Vahan sources candidate leads from 16 channels ("cohorts" = `lead_source`) and calls them to drive
conversion into FT. The raw data is candidate-level (18,198 rows, one row per candidate per
lead_source, 18 Jul – 6 Aug 2026) with funnel flags:

```
Uploaded → Attempted → Connected → Interested → Onboarded (OB) → FT
```

Three questions were asked:

1. Which 3 cohorts are best, and on what metric?
2. Write a SQL query that aggregates the raw data to a sensible level, and show the output.
3. Build an ML model showing which factors influence the chance of FT, including a confusion matrix.

## Repo contents

| File | Description |
|---|---|
| `Vahan_Case_Study_Assessment.pdf` | Full report — executive summary, methodology, findings, and recommendations for all 3 questions |
| `Vahan_Case_Study_Solution.docx` | Same report in editable Word format |
| `Q2_aggregation_query.sql` | SQL query aggregating raw candidate-level data to the `lead_source` (cohort) grain |
| `aggregated_lead_source.xlsx` | Output of the Q2 query, as a formatted spreadsheet |
| `Q3_ml_model.py` | Python script: feature engineering, Random Forest + Logistic Regression models, confusion matrix, feature importance |

## Results at a glance

**Q1 — Top 3 cohorts** (metric: `FT after Upload ÷ Uploaded Leads`)

| Rank | Cohort | FT Conversion % |
|---|---|---|
| 1 | Single Referral > 7 days - 24th Jul | 0.93% |
| 2 | Khanna - 2W 26th Jul | 0.91% |
| 3 | PreOb-Ob Fees Paid 29th Jul (set 1) | 0.47% |

**Q2 — Aggregation:** cohort-level (`lead_source`) grain, rates computed after `SUM()` (not row-averaged) to avoid weighting bias. See `Q2_aggregation_query.sql`.

**Q3 — ML model:** Random Forest (class-weighted, handles the 0.30% positive rate), predicting `FT_after_upload`.

- Precision (FT): 36.4% · Recall (FT): 85.7% · ROC-AUC: 0.934
- Top driver: `OB_after_upload` (onboarding) — by a wide margin, followed by call speed/persistence (`upload_to_first_attempt_P50`, `Attempt per Lead`)

## Methodology notes

- **Leakage avoidance:** `FT_after_first_attempt` and the pre-computed `→ %` columns were excluded from the model — they're row-level restatements of the target/funnel flags, not independent signal.
- **Class imbalance:** only 54/18,198 candidates (0.30%) converted, so accuracy is a misleading metric; the model was evaluated and tuned on precision/recall/ROC-AUC instead, with `class_weight="balanced"`.
- **Aggregation grain:** chosen at `lead_source` since each cohort here maps to a single sourcing batch/date. In a system where sources are reused across dates, `lead_source + upload_date` would be the better grain.

## Stack

- Python: `pandas`, `scikit-learn`, `matplotlib`
- SQL (ANSI-standard, tested logic in pandas equivalent)

---
<<<<<<< HEAD
*Vahan · Confidential — for candidate use only*
=======
>>>>>>> origin/main
