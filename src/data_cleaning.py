"""Data cleaning utilities for the sales dataset.

This module contains functions to load raw sales data, assess data
quality (missing values, duplicates, dtypes), clean the dataset, and
engineer features required for downstream KPI and EDA calculations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from src.utils import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "customer_name",
    "region",
    "category",
    "product_name",
    "quantity",
    "unit_price",
    "sales",
    "profit",
]


def load_raw_data(path: Path) -> pd.DataFrame:
    """Load the raw sales CSV file into a DataFrame.

    Args:
        path: Path to the raw CSV file.

    Returns:
        Raw, uncleaned DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {path}")

    df = pd.read_csv(path)
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {sorted(missing_cols)}")

    logger.info("Loaded raw data with shape %s from %s", df.shape, path)
    return df


def generate_data_quality_report(df: pd.DataFrame) -> Dict[str, object]:
    """Generate a summary data-quality report for the given DataFrame.

    Args:
        df: DataFrame to inspect.

    Returns:
        Dictionary summarizing shape, dtypes, missing values, and duplicates.
    """
    report: Dict[str, object] = {
        "n_rows": len(df),
        "n_columns": df.shape[1],
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "missing_pct": (df.isna().mean() * 100).round(2).to_dict(),
        "n_duplicate_rows": int(df.duplicated().sum()),
    }
    logger.info(
        "Data quality report: %s rows, %s duplicate rows",
        report["n_rows"],
        report["n_duplicate_rows"],
    )
    return report


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values using column-appropriate strategies.

    Numeric columns are imputed with the median; categorical/text
    columns are imputed with the string "Unknown"; rows missing a
    critical identifier (order_id) are dropped.

    Args:
        df: DataFrame with potential missing values.

    Returns:
        DataFrame with missing values handled.
    """
    df = df.copy()
    before = len(df)
    df = df.dropna(subset=["order_id"])
    dropped = before - len(df)
    if dropped:
        logger.info("Dropped %s rows missing order_id", dropped)

    numeric_cols = ["quantity", "unit_price", "sales", "profit"]
    for col in numeric_cols:
        if col in df.columns and df[col].isna().any():
            median_value = df[col].median()
            df[col] = df[col].fillna(median_value)
            logger.info("Filled missing values in %s with median=%.2f", col, median_value)

    categorical_cols = ["region", "category", "product_name", "customer_name"]
    for col in categorical_cols:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna("Unknown")
            logger.info("Filled missing values in %s with 'Unknown'", col)

    return df


def remove_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """Remove duplicate rows from the DataFrame.

    Args:
        df: Input DataFrame.
        subset: Optional list of columns to consider for duplication.

    Returns:
        DataFrame without duplicate rows.
    """
    before = len(df)
    df = df.drop_duplicates(subset=subset).reset_index(drop=True)
    removed = before - len(df)
    if removed:
        logger.info("Removed %s duplicate rows", removed)
    return df


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce columns to their expected data types.

    Args:
        df: Input DataFrame.

    Returns:
        DataFrame with corrected dtypes.
    """
    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").astype("Int64")
    for col in ["unit_price", "sales", "profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["order_id", "customer_id", "customer_name", "region", "category", "product_name"]:
        df[col] = df[col].astype("string")

    n_bad_dates = int(df["order_date"].isna().sum())
    if n_bad_dates:
        logger.warning("%s rows had unparseable order_date values", n_bad_dates)

    return df


def handle_outliers_iqr(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Cap outliers in the given numeric columns using the IQR method.

    Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR are clipped to
    those bounds rather than removed, to preserve row counts.

    Args:
        df: Input DataFrame.
        columns: Numeric columns to cap.

    Returns:
        DataFrame with outliers capped.
    """
    df = df.copy()
    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_outliers = int(((df[col] < lower) | (df[col] > upper)).sum())
        df[col] = df[col].clip(lower=lower, upper=upper)
        if n_outliers:
            logger.info("Capped %s outliers in column '%s'", n_outliers, col)
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived features required for KPI and EDA calculations.

    Adds order_month, order_year, order_value, and profit_margin columns.

    Args:
        df: Cleaned DataFrame with a datetime order_date column.

    Returns:
        DataFrame with engineered features.
    """
    df = df.copy()
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_value"] = df["sales"]
    df["profit_margin"] = np.where(df["sales"] != 0, df["profit"] / df["sales"], np.nan)
    return df


def clean_pipeline(raw_path: Path) -> tuple[pd.DataFrame, Dict[str, object]]:
    """Run the full cleaning pipeline on the raw sales data.

    Args:
        raw_path: Path to the raw CSV file.

    Returns:
        A tuple of (cleaned_dataframe, data_quality_report_before_cleaning).
    """
    raw_df = load_raw_data(raw_path)
    quality_report = generate_data_quality_report(raw_df)

    df = handle_missing_values(raw_df)
    df = remove_duplicates(df, subset=["order_id"])
    df = fix_data_types(df)
    df = handle_outliers_iqr(df, columns=["quantity", "unit_price", "sales", "profit"])
    df = engineer_features(df)

    logger.info("Cleaning pipeline complete. Final shape: %s", df.shape)
    return df, quality_report
