"""Chart generation for the sales analysis pipeline.

All functions save a matplotlib figure to disk and return the path,
so they can be used both from scripts and notebooks.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["figure.dpi"] = 120
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3


def _save_fig(fig: plt.Figure, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return out_path


def plot_monthly_sales_trend(monthly_summary: pd.DataFrame, out_path: Path) -> Path:
    """Line chart of monthly revenue."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_summary["order_month"], monthly_summary["total_sales"], marker="o", color="#2563eb")
    ax.set_title("Monthly Sales Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    ax.tick_params(axis="x", rotation=45)
    return _save_fig(fig, out_path)


def plot_revenue_by_region(regional_summary: pd.DataFrame, out_path: Path) -> Path:
    """Bar chart of revenue by region."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(regional_summary["region"], regional_summary["total_sales"], color="#16a34a")
    ax.set_title("Revenue by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Sales")
    return _save_fig(fig, out_path)


def plot_revenue_by_category(category_summary: pd.DataFrame, out_path: Path) -> Path:
    """Bar chart of revenue by category."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(category_summary["category"], category_summary["total_sales"], color="#ea580c")
    ax.set_title("Revenue by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Total Sales")
    ax.tick_params(axis="x", rotation=30)
    return _save_fig(fig, out_path)


def plot_top_n_bar(summary: pd.DataFrame, label_col: str, value_col: str, title: str, out_path: Path) -> Path:
    """Horizontal bar chart for top-N rankings (customers or products)."""
    fig, ax = plt.subplots(figsize=(9, 6))
    ordered = summary.sort_values(value_col)
    ax.barh(ordered[label_col], ordered[value_col], color="#7c3aed")
    ax.set_title(title)
    ax.set_xlabel(value_col.replace("_", " ").title())
    return _save_fig(fig, out_path)


def plot_order_value_distribution(df: pd.DataFrame, out_path: Path) -> Path:
    """Histogram of order values."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["order_value"], bins=30, color="#0891b2", edgecolor="white")
    ax.set_title("Order Value Distribution")
    ax.set_xlabel("Order Value")
    ax.set_ylabel("Frequency")
    return _save_fig(fig, out_path)


def plot_category_share_pie(category_summary: pd.DataFrame, out_path: Path) -> Path:
    """Pie chart of revenue share by category."""
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        category_summary["total_sales"],
        labels=category_summary["category"],
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.set_title("Revenue Share by Category")
    return _save_fig(fig, out_path)


def plot_quantity_vs_profit_scatter(df: pd.DataFrame, out_path: Path) -> Path:
    """Scatter plot of quantity sold vs. profit."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df["quantity"], df["profit"], alpha=0.6, color="#db2777")
    ax.set_title("Quantity vs. Profit")
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Profit")
    return _save_fig(fig, out_path)
