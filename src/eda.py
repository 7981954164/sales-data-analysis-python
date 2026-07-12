"""Exploratory data analysis functions for the sales dataset.

Each function returns a tidy pandas DataFrame or Series that can be
passed directly to the visualization module or exported to CSV.
"""

from __future__ import annotations

import pandas as pd


def monthly_sales_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and profit by order month.

    Args:
        df: Cleaned sales DataFrame with an order_month column.

    Returns:
        DataFrame indexed by order_month with sales and profit totals.
    """
    summary = (
        df.groupby("order_month", as_index=False)
        .agg(total_sales=("sales", "sum"), total_profit=("profit", "sum"), n_orders=("order_id", "nunique"))
        .sort_values("order_month")
        .reset_index(drop=True)
    )
    return summary


def regional_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue, profit, and order counts by region.

    Args:
        df: Cleaned sales DataFrame.

    Returns:
        DataFrame summarizing performance by region, sorted by revenue.
    """
    summary = (
        df.groupby("region", as_index=False)
        .agg(total_sales=("sales", "sum"), total_profit=("profit", "sum"), n_orders=("order_id", "nunique"))
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    summary["revenue_share_pct"] = (summary["total_sales"] / summary["total_sales"].sum() * 100).round(2)
    return summary


def category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue, profit, and margin by product category.

    Args:
        df: Cleaned sales DataFrame.

    Returns:
        DataFrame summarizing performance by category, sorted by revenue.
    """
    summary = (
        df.groupby("category", as_index=False)
        .agg(total_sales=("sales", "sum"), total_profit=("profit", "sum"), n_orders=("order_id", "nunique"))
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    summary["profit_margin_pct"] = (summary["total_profit"] / summary["total_sales"] * 100).round(2)
    summary["revenue_share_pct"] = (summary["total_sales"] / summary["total_sales"].sum() * 100).round(2)
    return summary


def customer_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue, profit, and order counts by customer.

    Args:
        df: Cleaned sales DataFrame.

    Returns:
        DataFrame summarizing performance by customer, sorted by revenue.
    """
    summary = (
        df.groupby(["customer_id", "customer_name"], as_index=False)
        .agg(total_sales=("sales", "sum"), total_profit=("profit", "sum"), n_orders=("order_id", "nunique"))
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def product_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue, profit, and quantity by product.

    Args:
        df: Cleaned sales DataFrame.

    Returns:
        DataFrame summarizing performance by product, sorted by revenue.
    """
    summary = (
        df.groupby("product_name", as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            total_profit=("profit", "sum"),
            total_quantity=("quantity", "sum"),
            n_orders=("order_id", "nunique"),
        )
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )
    return summary


def top_n_customers(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N customers by total revenue.

    Args:
        df: Cleaned sales DataFrame.
        n: Number of top customers to return.

    Returns:
        DataFrame with the top N customers.
    """
    return customer_analysis(df).head(n)


def top_n_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N products by total revenue.

    Args:
        df: Cleaned sales DataFrame.
        n: Number of top products to return.

    Returns:
        DataFrame with the top N products.
    """
    return product_analysis(df).head(n)


def monthly_growth_rate(monthly_summary: pd.DataFrame) -> pd.DataFrame:
    """Compute month-over-month revenue growth rate.

    Args:
        monthly_summary: Output of monthly_sales_summary().

    Returns:
        DataFrame with an added growth_rate_pct column.
    """
    result = monthly_summary.copy()
    result["growth_rate_pct"] = result["total_sales"].pct_change().mul(100).round(2)
    return result
