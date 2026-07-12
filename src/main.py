"""CLI entry point orchestrating the sales analysis pipeline.

Usage:
    python -m src.main --input data/raw/sample_sales_data.csv --outdir outputs
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src import eda, kpi, visualization
from src.data_cleaning import clean_pipeline
from src.utils import ensure_dir, get_logger

logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the sales data analysis pipeline.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/sample_sales_data.csv"),
        help="Path to the raw sales CSV file.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("outputs"),
        help="Directory to write summary tables and reports to.",
    )
    parser.add_argument(
        "--imagesdir",
        type=Path,
        default=Path("images"),
        help="Directory to write chart images to.",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directory to write the cleaned dataset to.",
    )
    return parser.parse_args()


def run(input_path: Path, outdir: Path, imagesdir: Path, processed_dir: Path) -> None:
    """Run the end-to-end pipeline: clean, analyze, visualize, export.

    Args:
        input_path: Path to the raw sales CSV file.
        outdir: Directory to write summary tables and reports to.
        imagesdir: Directory to write chart images to.
        processed_dir: Directory to write the cleaned dataset to.
    """
    ensure_dir(outdir)
    ensure_dir(imagesdir)
    ensure_dir(processed_dir)

    logger.info("Starting pipeline for %s", input_path)
    df, quality_report = clean_pipeline(input_path)

    cleaned_path = processed_dir / "cleaned_sales_data.csv"
    df.to_csv(cleaned_path, index=False)
    logger.info("Exported cleaned dataset to %s", cleaned_path)

    with open(outdir / "data_quality_report.json", "w", encoding="utf-8") as fh:
        json.dump(quality_report, fh, indent=2, default=str)

    monthly_summary = eda.monthly_sales_summary(df)
    monthly_growth = eda.monthly_growth_rate(monthly_summary)
    regional_summary = eda.regional_analysis(df)
    category_summary = eda.category_analysis(df)
    top_customers = eda.top_n_customers(df, n=10)
    top_products = eda.top_n_products(df, n=10)

    monthly_growth.to_csv(outdir / "monthly_sales_summary.csv", index=False)
    regional_summary.to_csv(outdir / "regional_summary.csv", index=False)
    category_summary.to_csv(outdir / "category_summary.csv", index=False)
    top_customers.to_csv(outdir / "top_10_customers.csv", index=False)
    top_products.to_csv(outdir / "top_10_products.csv", index=False)

    kpi_summary = kpi.build_kpi_summary(df)
    with open(outdir / "kpi_summary.json", "w", encoding="utf-8") as fh:
        json.dump(kpi_summary, fh, indent=2)
    logger.info("KPI summary: %s", kpi_summary)

    visualization.plot_monthly_sales_trend(monthly_summary, imagesdir / "monthly_sales_trend.png")
    visualization.plot_revenue_by_region(regional_summary, imagesdir / "revenue_by_region.png")
    visualization.plot_revenue_by_category(category_summary, imagesdir / "revenue_by_category.png")
    visualization.plot_top_n_bar(
        top_customers, "customer_name", "total_sales", "Top 10 Customers by Revenue", imagesdir / "top_10_customers.png"
    )
    visualization.plot_top_n_bar(
        top_products, "product_name", "total_sales", "Top 10 Products by Revenue", imagesdir / "top_10_products.png"
    )
    visualization.plot_order_value_distribution(df, imagesdir / "order_value_distribution.png")
    visualization.plot_category_share_pie(category_summary, imagesdir / "category_share_pie.png")
    visualization.plot_quantity_vs_profit_scatter(df, imagesdir / "quantity_vs_profit_scatter.png")

    logger.info("Pipeline complete. Outputs written to %s and %s", outdir, imagesdir)


def main() -> None:
    """Entry point for command-line execution."""
    args = parse_args()
    run(args.input, args.outdir, args.imagesdir, args.processed_dir)


if __name__ == "__main__":
    main()
