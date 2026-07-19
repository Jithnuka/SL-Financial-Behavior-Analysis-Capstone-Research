import pandas as pd

def credit_sources(df):
    credit_vars = {
        "Bank / Financial Institution": "borrow_bank",
        "Microfinance": "borrow_mfi",
        "Mobile / Digital Credit": "borrow_mobile",
        "Family / Friends": "borrow_family",
        "Informal Lender": "borrow_informal"
    }

    data = {}
    for name, col in credit_vars.items():
        if col in df.columns:
            data[name] = df[col].mean() * 100

    return pd.Series(data).sort_values(ascending=False)
