import pandas as pd


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy
    df = df.copy()

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    print('DEBUG preprocess: columns after normalize ->', list(df.columns))

    # Create gender from 'female' (1=Male,2=Female)
    if 'gender' not in df.columns and 'female' in df.columns:
        df['gender'] = df['female'].map({1: 'Male', 1.0: 'Male', 2: 'Female', 2.0: 'Female'})
        print('DEBUG preprocess: created gender column (head):', df['gender'].head().tolist())

    # income quintile
    if 'income_quintile' not in df.columns and 'inc_q' in df.columns:
        df['income_quintile'] = df['inc_q']

    # age group
    if 'age' in df.columns and 'age_group' not in df.columns:
        bins = [0, 24, 34, 44, 54, 64, 120]
        labels = ['<25', '25-34', '35-44', '45-54', '55-64', '65+']
        df['age_group'] = pd.cut(pd.to_numeric(df['age'], errors='coerce'), bins=bins, labels=labels)

    # borrow_any
    if 'borrow_any' not in df.columns:
        if 'borrowed' in df.columns:
            df['borrow_any'] = df['borrowed'].apply(lambda x: 1 if x == 1 else 0)
            print('DEBUG preprocess: created borrow_any (head):', df['borrow_any'].head().tolist())
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

    # Ensure borrow_* are 0/1
    for prefix in ['borrow_bank', 'borrow_mfi', 'borrow_mobile', 'borrow_family', 'borrow_informal']:
        if prefix in df.columns:
            df[prefix] = pd.to_numeric(df[prefix], errors='coerce').fillna(0).apply(lambda x: 1 if x == 1 else 0)

    return df
import pandas as pd


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize and derive columns used in the analysis.

    - normalize column names
    - create `gender`, `age_group`, `income_quintile`, `borrow_any`
    - derive `borrow_bank`, `borrow_mfi`, `borrow_mobile`, `borrow_family`, `borrow_informal`
    """
    df = df.copy()

    # Debug trace
    print('preprocess: starting, input columns:', list(df.columns)[:20])

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]
    print('preprocess: normalized columns:', list(df.columns)[:20])

    # gender
    if 'gender' not in df.columns and 'female' in df.columns:
        # map 1 -> Male, 2 -> Female; accept floats/ints
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

    # Ensure all borrow_* are 0/1
    for prefix in ['borrow_bank', 'borrow_mfi', 'borrow_mobile', 'borrow_family', 'borrow_informal']:
        if prefix in df.columns:
            df[prefix] = pd.to_numeric(df[prefix], errors='coerce').fillna(0).apply(lambda x: 1 if x == 1 else 0)

    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy
    df = df.copy()

    # Normalize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]

    # Gender: create `gender` column
    if 'gender' not in df.columns:
        if 'female' in df.columns:
            # Survey sometimes codes female as 1/2; map to Male/Female
            df['gender'] = df['female'].map({1: 'Male', 2: 'Female'})
        else:
            df['gender'] = pd.NA

    # Income quintile
    if 'income_quintile' not in df.columns and 'inc_q' in df.columns:
        df['income_quintile'] = df['inc_q']

    # Age groups
    if 'age' in df.columns and 'age_group' not in df.columns:
        bins = [0, 24, 34, 44, 54, 64, 120]
        labels = ['<25', '25-34', '35-44', '45-54', '55-64', '65+']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

    # borrow_any: prefer explicit 'borrowed' column
    if 'borrow_any' not in df.columns:
        if 'borrowed' in df.columns:
            # assume 1 means borrowed
            df['borrow_any'] = df['borrowed'].apply(lambda x: 1 if x == 1 else 0)
        else:
            # try common alternatives
            for alt in ['fin19', 'fin17a', 'fin17c']:
                if alt in df.columns:
                    df['borrow_any'] = df[alt].apply(lambda x: 1 if x == 1 else 0)
                    break

    # Create borrow source flags from fin22* if present
    fin22_map = {
        'fin22a': 'borrow_bank',
        'fin22b': 'borrow_mfi',
        'fin22d': 'borrow_mobile',
        'fin22e': 'borrow_family',
        'fin22f': 'borrow_informal'
    }

    for col, new_col in fin22_map.items():
        if col in df.columns and new_col not in df.columns:
            # many survey codes use 1=yes, 2=no. Treat 1 as True.
            df[new_col] = df[col].apply(lambda x: 1 if x == 1 else 0)

    # Coerce existing borrow_* columns to 0/1 where possible
    for prefix in ['borrow_bank', 'borrow_mfi', 'borrow_mobile', 'borrow_family', 'borrow_informal']:
        if prefix in df.columns:
            df[prefix] = pd.to_numeric(df[prefix], errors='coerce').fillna(0).apply(lambda x: 1 if x == 1 else 0)

    return df
import pandas as pd


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # Work on a copy
    df = df.copy()

    # Normalize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]

    # Gender: create `gender` column
    if 'gender' not in df.columns:
        if 'female' in df.columns:
            # Survey sometimes codes female as 1/2; map to Male/Female
            df['gender'] = df['female'].map({1: 'Male', 2: 'Female'})
        else:
            df['gender'] = pd.NA

    # Income quintile
    if 'income_quintile' not in df.columns and 'inc_q' in df.columns:
        df['income_quintile'] = df['inc_q']

    # Age groups
    if 'age' in df.columns and 'age_group' not in df.columns:
        bins = [0, 24, 34, 44, 54, 64, 120]
        labels = ['<25', '25-34', '35-44', '45-54', '55-64', '65+']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

    # borrow_any: prefer explicit 'borrowed' column
    if 'borrow_any' not in df.columns:
        if 'borrowed' in df.columns:
            # assume 1 means borrowed
            df['borrow_any'] = df['borrowed'].apply(lambda x: 1 if x == 1 else 0)
        else:
            # try common alternatives
            for alt in ['fin19', 'fin17a', 'fin17c']:
                if alt in df.columns:
                    df['borrow_any'] = df[alt].apply(lambda x: 1 if x == 1 else 0)
                    break

    # Create borrow source flags from fin22* if present
    fin22_map = {
        'fin22a': 'borrow_bank',
        'fin22b': 'borrow_mfi',
        'fin22d': 'borrow_mobile',
        'fin22e': 'borrow_family',
        'fin22f': 'borrow_informal'
    }

    for col, new_col in fin22_map.items():
        if col in df.columns and new_col not in df.columns:
            # many survey codes use 1=yes, 2=no. Treat 1 as True.
            df[new_col] = df[col].apply(lambda x: 1 if x == 1 else 0)

    # Coerce existing borrow_* columns to 0/1 where possible
    for prefix in ['borrow_bank', 'borrow_mfi', 'borrow_mobile', 'borrow_family', 'borrow_informal']:
        if prefix in df.columns:
            df[prefix] = pd.to_numeric(df[prefix], errors='coerce').fillna(0).apply(lambda x: 1 if x == 1 else 0)

    return df
import pandas as pd


def preprocess(df):
    # Placeholder for preprocessing steps
    return df
