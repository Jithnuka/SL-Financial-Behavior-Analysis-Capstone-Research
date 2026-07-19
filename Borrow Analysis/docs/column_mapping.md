## Summary of key mappings (applied automatically)

- `female` -> `gender` (mapped: 1→Male, 2→Female)
- `age` -> `age_group` (binned: `<25`, `25-34`, `35-44`, `45-54`, `55-64`, `65+`)
- `inc_q` -> `income_quintile`
- `borrowed` -> `borrow_any` (1 ⇒ borrowed)

Borrowing source mapping (from `fin22*`):

- `fin22a` -> `borrow_bank` (bank / financial institution)
- `fin22b` -> `borrow_mfi` (microfinance)
- `fin22d` -> `borrow_mobile` (mobile / digital credit)
- `fin22e` -> `borrow_family` (family / friends)
- `fin22f` -> `borrow_informal` (informal lender)

Purpose candidates detected:

- `fin24`, `fin24a`, `fin24b`, `fin24c`, `fin30`, `fin32` — these look like purpose indicators (1=yes)

## Computed sample statistics (from the CSV)

- Overall `borrow_any`: 54.2% of respondents indicated borrowing.

Borrow source prevalence (percent reporting each source):

- `borrow_bank` (from `fin22a`): 12.7%
- `borrow_mfi` (from `fin22b`): 20.6%
- `borrow_mobile` (from `fin22d`): 14.3%
- `borrow_family` (from `fin22e`): 6.1%
- `borrow_informal` (from `fin22f`): 36.1%

Purpose variable prevalences (each column: percent == 1):

# Column mapping report — Findex_Microdata_2025_Sri Lanka_Clean.csv

This document summarizes the column mappings and the computed prevalences derived from the uploaded CSV. The mappings were applied by `src/processing.py` and used by the analysis pipeline.

## Key mappings

- `female` -> `gender` (mapped: 1 → Male, 2 → Female)
- `age` -> `age_group` (binned: `<25`, `25-34`, `35-44`, `45-54`, `55-64`, `65+`)
- `inc_q` -> `income_quintile` (quintiles 1–5)
- `borrowed` -> `borrow_any` (1 ⇒ borrowed)

### Borrowing source mapping (from `fin22*`)

- `fin22a` -> `borrow_bank` (bank / financial institution)
- `fin22b` -> `borrow_mfi` (microfinance)
- `fin22d` -> `borrow_mobile` (mobile / digital credit)
- `fin22e` -> `borrow_family` (family / friends)
- `fin22f` -> `borrow_informal` (informal lender)

### Purpose candidates detected

The pipeline detected the following purpose-like columns: `fin24`, `fin24a`, `fin24b`, `fin24c`, `fin30`, `fin32`. These appear to be indicators (1 = yes) for one or more borrowing purposes. The exact labels should be verified with the official survey codebook.

## Computed sample statistics (from the CSV)

- Overall `borrow_any`: 54.2% of respondents indicated borrowing (derived from `borrowed`).

### Borrow source prevalence (percent reporting each source)

- `borrow_bank` (from `fin22a`): 12.7%
- `borrow_mfi` (from `fin22b`): 20.6%
- `borrow_mobile` (from `fin22d`): 14.3%
- `borrow_family` (from `fin22e`): 6.1%
- `borrow_informal` (from `fin22f`): 36.1%

### Purpose variable prevalences (each column: percent == 1)

- `fin24`: 10.3%
- `fin24a`: 44.8%
- `fin24b`: 30.9%
- `fin24c`: 24.4%
- `fin30`: 48.2%
- `fin32`: 26.5%

## How to update these values

To regenerate these statistics after preprocessing, run:

```bash
./myenv/bin/python -c "from src.load_data import load_data; from src.processing import preprocess; import pandas as pd; df=preprocess(load_data('data/Findex_Microdata_2025_Sri Lanka_Clean.csv')); print(df[['borrow_any','inc_q']].describe())"
```

## Notes

- The mappings and prevalences are heuristic and depend on how `src/processing.py` interprets `fin*` variables. Provide the official codebook to improve label accuracy.
