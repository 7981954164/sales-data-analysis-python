"""Business KPI calculations for the sales dataset."""

from __future__ import annotations

from typing import Dict

import pandas as pd


def total_revenue(df: pd.DataFrame) -> float:
    """Return total revenue (sum of sales)."""
    return float(df["sales"].sum())


def total_profit(df: pd.DataFrame) -> float:
    """Return total profit."""
    return float(df["profit"].sum())


def profit_margin_pct(df: pd.DataFrame) -> float:
    """Return overall profit margin as a percentage of revenue."""
    revenue = total_revenue(df)
    if revenue == 0:
        return 0.0
    return round(total_profit(df) / revenue * 100, 2)


def average_order_value(df: pd.DataFrame) -> float:
    """Return average order value (revenue / number of unique orders)."""
    n_orders = df["order_id"].nunique()
    if n_orders == 0:
        return 0.0
    return round(total_revenue(df) / n_orders, 2)


def total_orders(df: pd.DataFrame) -> int:
    """Return the number of unique orders."""
    return int(df["order_id"].nunique())


def total_customers(df: pd.DataFrame) -> int:
    """Return the number of unique customers."""
    return int(df["customer_id"].nunique())


def build_kpi_summary(df: pd.DataFrame) -> Dict[str, float]:
    """Compute the full set of headline business KPIs.

    Args:
        df: Cleaned, feature-engineered sales DataFrame.

    Returns:
        Dictionary of KPI name to value, ready for export or display.
    """
    return {
        "total_revenue": total_revenue(df),
        "total_profit": total_profit(df),
        "profit_margin_pct": profit_margin_pct(df),
        "average_order_value": average_order_value(df),
        "total_orders": total_orders(df),
        "total_customers": total_customers(df),
    }
