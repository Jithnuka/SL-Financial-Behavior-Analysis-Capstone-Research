import matplotlib.pyplot as plt
import os
import pandas as pd


def bar_plot(series, title, filename):
    # Ensure we have a numeric series; skip gracefully if not
    if not isinstance(series, pd.Series):
        try:
            series = pd.Series(series)
        except Exception:
            print(f"Skipping plot '{title}': series is not convertible to a Series")
            return

    series = pd.to_numeric(series, errors='coerce')
    series = series.dropna()

    if series.empty:
        print(f"Skipping plot '{title}': no numeric data to plot")
        return

    plt.figure()
    series.plot(kind='bar')
    plt.title(title)
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    os.makedirs("output/figures", exist_ok=True)
    plt.savefig(f"output/figures/{filename}")
    plt.close()
