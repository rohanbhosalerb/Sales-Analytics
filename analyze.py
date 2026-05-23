"""
Sales Data Analyzer
--------------------
Performs EDA, cleans data, and generates visualizations from sales_data.csv.

Usage:
    python analyze.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import warnings

warnings.filterwarnings("ignore")

# ── Config ──────────────────────────────────────────────────────────────────
DATA_PATH = "data/sales_data.csv"
OUTPUT_DIR = "outputs"
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── 1. Load & Inspect ────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    print("=" * 55)
    print("📦  DATASET OVERVIEW")
    print("=" * 55)
    print(f"  Rows      : {df.shape[0]:,}")
    print(f"  Columns   : {df.shape[1]}")
    print(f"  Date range: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"\n  Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0].to_string()}")
    return df


# ── 2. Clean ─────────────────────────────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.dropna(subset=["unit_price", "quantity"])
    df["discount"] = df["discount"].fillna(0.0)
    df["revenue"] = (df["unit_price"] * df["quantity"] * (1 - df["discount"])).round(2)
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    print(f"\n🧹  Cleaned: dropped {before - len(df)} incomplete rows → {len(df):,} remaining")
    return df


# ── 3. Summary Stats ─────────────────────────────────────────────────────────
def summary_stats(df: pd.DataFrame):
    total_rev = df["revenue"].sum()
    avg_order = df["revenue"].mean()
    top_cat = df.groupby("category")["revenue"].sum().idxmax()

    print("\n" + "=" * 55)
    print("📊  KEY METRICS")
    print("=" * 55)
    print(f"  Total Revenue   : ${total_rev:,.2f}")
    print(f"  Avg Order Value : ${avg_order:,.2f}")
    print(f"  Top Category    : {top_cat}")

    print("\n  Revenue by Region:")
    region_rev = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
    for r, v in region_rev.items():
        print(f"    {r:<8} ${v:,.2f}")

    print("\n  Revenue by Category:")
    cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
    for c, v in cat_rev.items():
        print(f"    {c:<15} ${v:,.2f}")


# ── 4. Visualisations ────────────────────────────────────────────────────────
def plot_monthly_revenue(df: pd.DataFrame):
    monthly = (
        df.groupby("month_num")["revenue"]
        .sum()
        .reset_index()
        .sort_values("month_num")
    )
    month_labels = pd.to_datetime(monthly["month_num"], format="%m").dt.strftime("%b")

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.fill_between(range(len(monthly)), monthly["revenue"], alpha=0.25, color="#4C72B0")
    ax.plot(range(len(monthly)), monthly["revenue"], marker="o", linewidth=2.2, color="#4C72B0")
    ax.set_xticks(range(len(monthly)))
    ax.set_xticklabels(month_labels)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.set_title("Monthly Revenue (2023)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "monthly_revenue.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  📈  Saved: {path}")


def plot_category_breakdown(df: pd.DataFrame):
    cat_rev = df.groupby("category")["revenue"].sum().sort_values()

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Bar chart
    colors = sns.color_palette("muted", len(cat_rev))
    axes[0].barh(cat_rev.index, cat_rev.values, color=colors)
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}k"))
    axes[0].set_title("Revenue by Category", fontweight="bold")
    axes[0].set_xlabel("Revenue ($)")

    # Pie chart
    axes[1].pie(
        cat_rev.values,
        labels=cat_rev.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        pctdistance=0.82,
    )
    axes[1].set_title("Revenue Share by Category", fontweight="bold")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "category_breakdown.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  🍕  Saved: {path}")


def plot_region_heatmap(df: pd.DataFrame):
    pivot = df.pivot_table(
        index="region", columns="category", values="revenue", aggfunc="sum"
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".0f",
        cmap="YlOrRd",
        linewidths=0.5,
        ax=ax,
        cbar_kws={"label": "Revenue ($)"},
    )
    ax.set_title("Revenue Heatmap — Region × Category", fontsize=13, fontweight="bold")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "region_category_heatmap.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  🗺️   Saved: {path}")


def plot_discount_impact(df: pd.DataFrame):
    bins = [-0.01, 0.0, 0.05, 0.10, 0.15, 0.20]
    labels = ["0%", "5%", "10%", "15%", "20%"]
    df["discount_bin"] = pd.cut(df["discount"], bins=bins, labels=labels)

    grouped = df.groupby("discount_bin", observed=True).agg(
        avg_revenue=("revenue", "mean"),
        order_count=("order_id", "count"),
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax2 = ax1.twinx()

    ax1.bar(grouped["discount_bin"], grouped["avg_revenue"], color="#4C72B0", alpha=0.75, label="Avg Revenue")
    ax2.plot(grouped["discount_bin"], grouped["order_count"], marker="s", color="#DD8452", linewidth=2, label="Orders")

    ax1.set_ylabel("Avg Revenue ($)", color="#4C72B0")
    ax2.set_ylabel("Order Count", color="#DD8452")
    ax1.set_xlabel("Discount Applied")
    ax1.set_title("Discount Level vs Avg Revenue & Order Volume", fontweight="bold")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "discount_impact.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  💸  Saved: {path}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    df = load_data(DATA_PATH)
    df = clean_data(df)
    summary_stats(df)

    print("\n" + "=" * 55)
    print("🎨  GENERATING CHARTS")
    print("=" * 55)
    plot_monthly_revenue(df)
    plot_category_breakdown(df)
    plot_region_heatmap(df)
    plot_discount_impact(df)

    print("\n✅  Analysis complete! Check the 'outputs/' folder.\n")


if __name__ == "__main__":
    main()
