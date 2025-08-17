from __future__ import annotations
import os
import warnings
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.simplefilter("ignore", category=FutureWarning)
sns.set_context("talk")

# ---------- IO & INFO ----------

def load_data(path: str) -> pd.DataFrame:
    """Load CSV to DataFrame with minimal dtype hygiene."""
    df = pd.read_csv(path)
    # Ensure revenue numeric
    if "revenue" in df.columns:
        df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    return df

def print_brief_info(df: pd.DataFrame, note: str = "") -> None:
    """Print concise info helpful for logs."""
    print(f"\n=== DataFrame info {f'({note})' if note else ''} ===")
    print(f"Shape: {df.shape}")
    nulls = df.isna().sum()
    if "revenue" in df.columns:
        print(f"Nulls in 'revenue': {int(nulls.get('revenue', 0))}")
    print("Columns:", list(df.columns))

# ---------- CLEANING ----------

_ALLOWED_METHODS = ["Email", "Call", "Email + Call"]

def _standardize_sales_method(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "sales_method" not in df.columns:
        return df
    # Normalize whitespace & case, then map to canonical labels
    sm = df["sales_method"].astype(str).str.strip().str.lower()
    mapped = sm.replace({
        "email": "Email",
        "call": "Call",
        "email + call": "Email + Call",
        "em + call": "Email + Call",
    })
    df["sales_method"] = mapped
    # Keep only allowed values
    df = df[df["sales_method"].isin(_ALLOWED_METHODS)]
    return df

def _clean_years_as_customer(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "years_as_customer" not in df.columns:
        return df
    # Keep values within [0, 41]
    df = df[(df["years_as_customer"] >= 0) & (df["years_as_customer"] <= 41)]
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning steps."""
    out = df.copy()

    # 1) Drop rows with missing revenue (expected: 1074)
    if "revenue" in out.columns:
        before = len(out)
        out = out.dropna(subset=["revenue"])
        print(f"Dropped {before - len(out)} rows with null 'revenue'.")

    # 2) Standardize & filter sales_method
    before = len(out)
    out = _standardize_sales_method(out)
    print(f"Filtered {before - len(out)} rows due to invalid 'sales_method' values.")

    # 3) Constrain years_as_customer to [0, 41] (expected: removes 2)
    before = len(out)
    out = _clean_years_as_customer(out)
    print(f"Removed {before - len(out)} rows outside 'years_as_customer' bounds.")

    # 4) Week coercion for plotting consistency
    if "week" in out.columns:
        # Try numeric first; fallback leaves as-is
        wk = pd.to_numeric(out["week"], errors="ignore")
        # If still object and looks like 'YYYY-WW', keep as string but ordered later
        out["week"] = wk

    return out

# ---------- PLOTTING UTILITIES ----------

def _ensure_outdir(outdir: Optional[str]) -> str:
    outdir = outdir or "figures"
    os.makedirs(outdir, exist_ok=True)
    return outdir

def _add_bar_labels(ax):
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{int(height) if pd.notna(height) else ''}",
                    (p.get_x() + p.get_width() / 2, height),
                    ha="center", va="bottom", xytext=(0, 3), textcoords="offset points")

# ---------- EDA PLOTS ----------

def eda_plots(df: pd.DataFrame, outdir: Optional[str] = "figures", show: bool = False) -> None:
    """Core EDA figures."""
    outdir = _ensure_outdir(outdir)

    # 1) Number of customers by sales method
    plt.figure(figsize=(7, 5))
    ax = sns.countplot(data=df, x="sales_method", order=["Email", "Call", "Email + Call"])
    plt.title("Number of Customers by Sales Method")
    _add_bar_labels(ax)
    plt.tight_layout()
    path = os.path.join(outdir, "count_customers_by_sales_method.png")
    plt.savefig(path, dpi=150)
    if show: plt.show()
    plt.close()

    # 2a) Distribution of revenue (overall)
    plt.figure(figsize=(7, 5))
    sns.histplot(df["revenue"], kde=True)
    plt.title("Distribution of Revenue (Overall)")
    plt.tight_layout()
    path = os.path.join(outdir, "distribution_revenue_overall.png")
    plt.savefig(path, dpi=150)
    if show: plt.show()
    plt.close()

    # 2b) Revenue by method — boxplot
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="sales_method", y="revenue", order=["Email", "Call", "Email + Call"])
    plt.title("Revenue Distribution by Sales Method")
    plt.tight_layout()
    path = os.path.join(outdir, "revenue_by_method_boxplot.png")
    plt.savefig(path, dpi=150)
    if show: plt.show()
    plt.close()

    # 3) Average weekly revenue by method
    if {"week", "revenue", "sales_method"}.issubset(df.columns):
        # Coerce week to an ordered axis
        if pd.api.types.is_numeric_dtype(df["week"]):
            sort_key = "week"
        else:
            # Keep natural string order
            sort_key = None

        plt.figure(figsize=(9, 5))
        sns.lineplot(
            data=df,
            x="week",
            y="revenue",
            hue="sales_method",
            estimator="mean",
            errorbar=None,
            sort=bool(sort_key),
        )
        plt.title("Average Weekly Revenue by Sales Method")
        plt.tight_layout()
        path = os.path.join(outdir, "avg_weekly_revenue_by_method.png")
        plt.savefig(path, dpi=150)
        if show: plt.show()
        plt.close()

# ---------- BUSINESS METRIC ----------

def business_metric_plot(df: pd.DataFrame, outdir: Optional[str] = "figures", show: bool = False) -> pd.DataFrame:
    """
    Compute and plot: Average Revenue per Customer per Sales Method.
    Returns the summary DataFrame (useful for reporting/tests).
    """
    outdir = _ensure_outdir(outdir)
    metric = (
        df.groupby("sales_method", as_index=False)["revenue"]
          .mean()
          .sort_values("revenue", ascending=False)
    )

    plt.figure(figsize=(7, 5))
    ax = sns.barplot(data=metric, x="sales_method", y="revenue",
                     order=["Email", "Call", "Email + Call"])
    plt.title("Average Revenue per Customer per Sales Method")
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f"{height:.2f}",
                    (p.get_x() + p.get_width()/2, height),
                    ha="center", va="bottom", xytext=(0, 3), textcoords="offset points")
    plt.tight_layout()
    path = os.path.join(outdir, "avg_revenue_per_customer_by_method.png")
    plt.savefig(path, dpi=150)
    if show: plt.show()
    plt.close()
    return metric
