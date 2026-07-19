import pandas as pd


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize and derive columns used in the analysis.

    Creates:
    - `gender` (from `female` where available)
    - `age_group` (binned)
    - `income_quintile` (from `inc_q`)
    - `borrow_any` (from `borrowed` or alternatives)
    - `borrow_bank`, `borrow_mfi`, `borrow_mobile`, `borrow_family`, `borrow_informal`
    """
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    # gender
    if 'gender' not in df.columns and 'female' in df.columns:
        df['gender'] = df['female'].map({1: 'Male', 1.0: 'Male', 2: 'Female', 2.0: 'Female'})

    # income_quintile
    if 'income_quintile' not in df.columns and 'inc_q' in df.columns:
        df['income_quintile'] = df['inc_q']

    # age_group
    if 'age' in df.columns and 'age_group' not in df.columns:
        bins = [0, 24, 34, 44, 54, 64, 120]
        labels = ['<25', '25-34', '35-44', '45-54', '55-64', '65+']
        df['age_group'] = pd.cut(pd.to_numeric(df['age'], errors='coerce'), bins=bins, labels=labels)

    # borrow_any
    if 'borrow_any' not in df.columns:
        if 'borrowed' in df.columns:
            df['borrow_any'] = df['borrowed'].apply(lambda x: 1 if x == 1 else 0)
        else:
            for alt in ['fin19', 'fin17a', 'fin17c']:
                if alt in df.columns:
                    df['borrow_any'] = df[alt].apply(lambda x: 1 if x == 1 else 0)
                    break

    # Borrowing sources from fin22* if present
    fin22_map = {
        'fin22a': 'borrow_bank',
        'fin22b': 'borrow_mfi',
        'fin22d': 'borrow_mobile',
        'fin22e': 'borrow_family',
        'fin22f': 'borrow_informal'
    }
    for col, new_col in fin22_map.items():
        if col in df.columns and new_col not in df.columns:
            df[new_col] = df[col].apply(lambda x: 1 if x == 1 else 0)

    for prefix in ['borrow_bank', 'borrow_mfi', 'borrow_mobile', 'borrow_family', 'borrow_informal']:
        if prefix in df.columns:
            df[prefix] = pd.to_numeric(df[prefix], errors='coerce').fillna(0).apply(lambda x: 1 if x == 1 else 0)

    return df
