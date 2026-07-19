import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


def _bootstrap_proportion(series, n_boot=1000, random_state=0):
    rng = np.random.default_rng(random_state)
    arr = np.asarray(series)
    arr = arr[~np.isnan(arr)]
    if arr.size == 0:
        return (0.0, 0.0, 0.0)
    boot = rng.choice(arr, size=(n_boot, arr.size), replace=True)
    props = boot.mean(axis=1)
    lower = np.percentile(props, 2.5) * 100
    upper = np.percentile(props, 97.5) * 100
    est = arr.mean() * 100
    return est, lower, upper


def income_quintile_plot(df: pd.DataFrame,
                         income_col: str = 'inc_q',
                         borrow_col: str = 'borrow_any',
                         map_names: Optional[dict] = None,
                         replace_with_names: bool = False,
                         show_both: bool = False,
                         annotate_counts: bool = True,
                         ci_boot: bool = True,
                         n_boot: int = 2000,
                         split_by: Optional[str] = None,
                         out_png: str = 'output/figures/borrow_income_advanced.png',
                         out_html: str = 'output/figures/borrow_income_advanced.html') -> None:
    """Create an advanced income-quintile plot.

    - `map_names`: mapping from code->name
    - `replace_with_names`: if True, x ticks are names only
    - `show_both`: if True, tick label shows '1 - Poorest'
    - `annotate_counts`: show sample size per bar
    - `ci_boot`: compute 95% CI via bootstrap
    - `split_by`: if provided, produce grouped bars by that column (e.g., 'gender' or 'age_group')
    """
    os.makedirs(os.path.dirname(out_png), exist_ok=True)

    df2 = df.copy()
    if income_col not in df2.columns or borrow_col not in df2.columns:
        raise ValueError('income_col or borrow_col missing')

    # Prepare group order
    groups = sorted(df2[income_col].dropna().unique(), key=lambda x: (int(x) if str(x).isdigit() else x))

    # Label mapping
    if map_names is None:
        map_names = {1: 'Poorest', 2: 'Lower-middle', 3: 'Middle', 4: 'Upper-middle', 5: 'Richest'}

    if split_by and split_by in df2.columns:
        # grouped bar: compute proportions and CIs per (income, split)
        split_vals = sorted(df2[split_by].dropna().unique())
        # build table
        table = {}
        ci_table = {}
        counts = {}
        for s in split_vals:
            table[s] = []
            ci_table[s] = []
            counts[s] = []
            for g in groups:
                subset = df2[(df2[income_col] == g) & (df2[split_by] == s)][borrow_col]
                est, lo, hi = _bootstrap_proportion(subset, n_boot=n_boot)
                table[s].append(est)
                ci_table[s].append((lo, hi))
                counts[s].append(int(subset.count()))

        # Plot static grouped bar with CI
        x = np.arange(len(groups))
        width = 0.8 / max(1, len(split_vals))
        fig, ax = plt.subplots(figsize=(9, 6))
        for i, s in enumerate(split_vals):
            offsets = x - 0.4 + i * width + width / 2
            ax.bar(offsets, table[s], width, label=str(s), yerr=np.transpose([[est - lo for (lo, hi), est in zip(ci_table[s], table[s])],[hi - est for (lo, hi), est in zip(ci_table[s], table[s])]]).T if ci_boot else None, capsize=5)
            if annotate_counts:
                for xi, val, cnt in zip(offsets, table[s], counts[s]):
                    ax.text(xi, val + 1.5, f'n={cnt}', ha='center', va='bottom', fontsize=8)

        # X ticks
        if replace_with_names:
            labels = [map_names.get(int(g), str(g)) for g in groups]
        elif show_both:
            labels = [f"{g} - {map_names.get(int(g), str(g))}" for g in groups]
        else:
            labels = [str(g) for g in groups]

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel('Percentage (%)')
        ax.set_title('Borrowing by Income Group')
        ax.legend(title=split_by)
        plt.tight_layout()
        fig.savefig(out_png)
        plt.close(fig)

        # Interactive plotly
        if PLOTLY_AVAILABLE:
            figp = go.Figure()
            for i, s in enumerate(split_vals):
                figp.add_trace(go.Bar(x=labels, y=table[s], name=str(s), error_y=dict(type='data', array=[hi - est for (lo, hi), est in zip(ci_table[s], table[s])], arrayminus=[est - lo for (lo, hi), est in zip(ci_table[s], table[s])]), text=[f'n={c}' for c in counts[s]]))
            figp.update_layout(barmode='group', title='Borrowing by Income Group (interactive)', yaxis_title='Percentage (%)')
            figp.write_html(out_html, include_plotlyjs='cdn')

    else:
        # simple bars per group
        ests = []
        ci_l = []
        ci_u = []
        counts = []
        for g in groups:
            subset = df2[df2[income_col] == g][borrow_col]
            est, lo, hi = _bootstrap_proportion(subset, n_boot=n_boot)
            ests.append(est)
            ci_l.append(lo)
            ci_u.append(hi)
            counts.append(int(subset.count()))

        x = np.arange(len(groups))
        fig, ax = plt.subplots(figsize=(8, 6))
        yerr = [np.array(ests) - np.array(ci_l), np.array(ci_u) - np.array(ests)] if ci_boot else None
        bars = ax.bar(x, ests, yerr=yerr if ci_boot else None, capsize=5)

        if annotate_counts:
            for xi, bar, cnt in zip(x, bars, counts):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5, f'n={cnt}', ha='center', va='bottom', fontsize=8)

        # labels
        if replace_with_names:
            labels = [map_names.get(int(g), str(g)) for g in groups]
        elif show_both:
            labels = [f"{g} - {map_names.get(int(g), str(g))}" for g in groups]
        else:
            labels = [str(g) for g in groups]

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel('Percentage (%)')
        ax.set_xlabel(income_col)
        ax.set_title('Borrowing by Income Group')
        plt.tight_layout()
        fig.savefig(out_png)
        plt.close(fig)

        if PLOTLY_AVAILABLE:
            figp = go.Figure()
            figp.add_trace(go.Bar(x=labels, y=ests, error_y=dict(type='data', array=np.array(ci_u) - np.array(ests), arrayminus=np.array(ests) - np.array(ci_l)), text=[f'n={c}' for c in counts]))
            figp.update_layout(title='Borrowing by Income Group (interactive)', yaxis_title='Percentage (%)')
            figp.write_html(out_html, include_plotlyjs='cdn')
