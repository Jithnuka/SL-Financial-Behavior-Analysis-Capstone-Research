import pandas as pd

def demographic_analysis(df, group_col, borrow_col):
    
    if group_col not in df.columns or borrow_col not in df.columns:
        print(f"Skipping demographic analysis for {group_col}/{borrow_col}: missing columns")
        return pd.Series(dtype=float)

    result = df.groupby(group_col)[borrow_col].mean() * 100
    return result.sort_values(ascending=False)
