import pandas as pd

def borrowing_purpose(df):
    # Prefer explicitly named columns if present
    purpose_cols = {
        "Education": "borrow_edu",
        "Health": "borrow_health",
        "Business": "borrow_business",
        "Consumption": "borrow_consumption",
        "Emergency": "borrow_emergency"
    }

    data = {}
    for label, col in purpose_cols.items():
        if col in df.columns:
            data[label] = df[col].mean() * 100

    if not data:
        candidates = [c for c in df.columns if c.lower().startswith('fin24') or c.lower().startswith('fin30') or c.lower().startswith('fin32')]
        for c in candidates:
            # treat value==1 as yes
            try:
                pct = (df[c] == 1).mean() * 100
            except Exception:
                continue
            # make label nicer
            label = c
            data[label] = pct

    return pd.Series(data).sort_values(ascending=False)
