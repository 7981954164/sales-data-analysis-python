# Sales Data Analysis using Python

![Python](https://img.shields.io/badge/Python-3.13-blue.svg) ![Pandas](https://img.shields.io/badge/Pandas-2.x-150458.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) ![Status](https://img.shields.io/badge/Status-Portfolio%20Project-orange.svg)

A production-style, end-to-end data analytics project that cleans, explores, and derives business KPIs from a retail sales dataset using Python, pandas, NumPy, and Matplotlib.

**Note on outputs:** This repository ships with a small, hand-authored sample dataset (`data/raw/sample_sales_data.csv`) and fully implemented analysis code in `src/`. The charts, tables, and figures referenced under `outputs/` and `images/` are generated when you run the pipeline (`python -m src.main`) against your own or the sample data. They are not pre-computed or bundled as static claims in this README. Any example numbers below are illustrative placeholders describing the shape of the analysis, not verified results.

## Table of Contents
- [Business Problem](#business-problem)
- - [Objectives](#objectives)
  - - [Key Performance Indicators](#key-performance-indicators)
    - - [Project Structure](#project-structure)
      - - [Dataset](#dataset)
        - - [Installation](#installation)
          - - [Usage](#usage)
            - - [Analysis Workflow](#analysis-workflow)
              - - [Sample Visualizations](#sample-visualizations)
                - - [Business Insights](#business-insights)
                  - - [Business Recommendations](#business-recommendations)
                    - - [Future Improvements](#future-improvements)
                      - - [License](#license)
                       
                        - ## Business Problem
                       
                        - A mid-size retail company sells products across multiple regions and categories. Leadership lacks a consolidated, repeatable way to understand monthly sales performance, profitability, top customers, and product-level trends. This project builds a reusable Python analytics pipeline that ingests raw transactional sales data, cleans it, and produces business-ready KPIs, charts, and a cleaned dataset suitable for BI tools such as Power BI or Tableau.
                       
                        - ## Objectives
                       
                        - 1. Build a reliable, reusable data-cleaning pipeline covering missing values, duplicates, outliers, and data types.
                          2. 2. Engineer features needed for time-series and profitability analysis such as order month, profit margin, and order value.
                             3. 3. Compute core business KPIs including revenue, profit margin, average order value, and growth trends.
                                4. 4. Identify top customers, top products, and best-performing regions and categories.
                                   5. 5. Produce clean, presentation-quality charts and export a BI-ready cleaned dataset.
                                      6. 6. Translate findings into concrete, actionable business recommendations.
                                        
                                         7. ## Key Performance Indicators
                                        
                                         8. | KPI | Description |
                                         9. |---|---|
                                         10. | Total Revenue | Sum of order sales value |
                                         11. | Total Profit | Sum of profit across orders |
                                         12. | Profit Margin % | Profit divided by Revenue |
                                         13. | Average Order Value (AOV) | Revenue divided by number of orders |
                                         14. | Monthly Revenue Growth % | Month-over-month revenue change |
                                         15. | Top 10 Customers by Revenue | Ranked customer contribution |
                                         16. | Top 10 Products by Revenue | Ranked product contribution |
                                         17. | Regional Revenue Share | Revenue percent by region |
                                         18. | Category Revenue Share | Revenue percent by category |
                                        
                                         19. ## Project Structure
                                        
                                         20. ```
                                             sales-data-analysis-python/
                                             assets/                  - design assets such as banners and icons
                                             data/raw/                - original or sample raw data
                                             data/processed/          - cleaned data exported by the pipeline
                                             images/                  - exported chart images (PNG)
                                             notebooks/               - demo notebook showing usage of src/
                                             outputs/                 - exported summary tables and reports
                                             src/__init__.py
                                             src/data_cleaning.py     - missing values, duplicates, outliers, dtypes
                                             src/eda.py               - exploratory analysis and aggregations
                                             src/kpi.py               - business KPI calculations
                                             src/visualization.py     - chart generation using matplotlib
                                             src/utils.py             - shared helpers and logging setup
                                             src/main.py              - CLI entry point orchestrating the pipeline
                                             .gitignore
                                             LICENSE
                                             requirements.txt
                                             README.md
                                             ```

                                             ## Dataset

                                             The sample dataset (`data/raw/sample_sales_data.csv`) is a small, hand-authored dataset that mirrors the structure of a typical retail sales export, with the following columns:

                                             | Column | Type | Description |
                                             |---|---|---|
                                             | order_id | string | Unique order identifier |
                                             | order_date | date | Date the order was placed |
                                             | customer_id | string | Unique customer identifier |
                                             | customer_name | string | Customer full name |
                                             | region | string | Sales region such as North, South, East, West |
                                             | category | string | Product category |
                                             | product_name | string | Product sold |
                                             | quantity | integer | Units sold |
                                             | unit_price | float | Price per unit |
                                             | sales | float | Total sales value for the line item |
                                             | profit | float | Profit for the line item |

                                             To use your own data, replace the CSV in `data/raw/` with a file following this schema, or adjust the column mapping in `src/data_cleaning.py`.

                                             ## Installation

                                             ```bash
                                             git clone https://github.com/7981954164/sales-data-analysis-python.git
                                             cd sales-data-analysis-python

                                             python -m venv .venv
                                             source .venv/bin/activate

                                             pip install -r requirements.txt
                                             ```

                                             On Windows, activate the virtual environment with `.venv\Scripts\activate` instead.

                                             ## Usage

                                             ```bash
                                             python -m src.main --input data/raw/sample_sales_data.csv --outdir outputs
                                             ```

                                             This will load and clean the raw CSV, export the cleaned dataset to `data/processed/cleaned_sales_data.csv`, compute KPIs and export summary tables to `outputs/`, and generate and save charts to `images/`.

                                             You can also open `notebooks/01_sales_analysis_demo.ipynb` to see a guided, cell-by-cell walkthrough of the same pipeline using the functions in `src/`.

                                             ## Analysis Workflow

                                             1. Data Understanding: inspect schema, dtypes, missing values, and duplicates.
                                             2. 2. Data Cleaning: impute or drop missing values, fix dtypes, remove duplicates, cap outliers using the IQR method.
                                                3. 3. Feature Engineering: derive order_month, profit_margin, order_value, and year.
                                                   4. 4. Exploratory Data Analysis: monthly sales, regional and category breakdowns, customer and product rankings.
                                                      5. 5. KPI Computation: revenue, profit, AOV, margin, and growth trends.
                                                         6. 6. Visualization: bar, line, histogram, scatter, and pie charts saved as PNGs.
                                                            7. 7. Insights and Recommendations: written up in this README and outputs/business_insights.md.
                                                              
                                                               8. ## Sample Visualizations
                                                              
                                                               9. Running the pipeline generates charts such as:
                                                              
                                                               10. - images/monthly_sales_trend.png - line chart of monthly revenue
                                                                   - - images/revenue_by_region.png - bar chart of regional performance
                                                                     - - images/revenue_by_category.png - bar chart of category performance
                                                                       - - images/top_10_customers.png - horizontal bar chart of top customers
                                                                         - - images/top_10_products.png - horizontal bar chart of top products
                                                                           - - images/order_value_distribution.png - histogram of order values
                                                                             - - images/category_share_pie.png - pie chart of category revenue share
                                                                               - - images/quantity_vs_profit_scatter.png - scatter plot of quantity vs profit
                                                                                
                                                                                 - These are generated locally when you run python -m src.main. They are not committed as pre-rendered images since no code has been executed in this environment.
                                                                                
                                                                                 - ## Business Insights
                                                                                
                                                                                 - The following are illustrative example insight statements in the format the pipeline is designed to produce. Run the pipeline on real data to generate verified, numeric findings for your own dataset.
                                                                                
                                                                                 - 1. Revenue tends to concentrate in a small number of top customers, so account management matters.
                                                                                   2. 2. A handful of product categories typically drive the majority of profit, not just revenue.
                                                                                      3. 3. Some high-revenue products can carry thin margins, while lower-revenue products can be highly profitable.
                                                                                         4. 4. Regional performance often varies more due to mix of categories sold than raw demand.
                                                                                            5. 5. Monthly revenue trends can reveal seasonality that supports inventory and staffing planning.
                                                                                               6. 6. Average order value is a useful lever distinct from raw order count for revenue growth.
                                                                                                  7. 7. A small share of products can generate a disproportionate share of returns and discount risk.
                                                                                                     8. 8. Customer repeat-purchase patterns can indicate loyalty versus one-time buyers.
                                                                                                        9. 9. Outlier orders with very large quantity or value can distort averages if not handled carefully.
                                                                                                           10. 10. Category-level profit margin differences often justify differentiated pricing or promotion strategy.
                                                                                                               11. 11. Top 10 customers versus long-tail customers analysis helps prioritize retention efforts.
                                                                                                                   12. 12. Product-level profit ranking can differ substantially from product-level revenue ranking.
                                                                                                                       13. 13. Growth trends month-over-month highlight whether recent performance is accelerating or slowing.
                                                                                                                           14. 14. Regional category mix analysis can reveal under-served, high-potential combinations.
                                                                                                                               15. 15. Order value distribution skew can inform minimum order thresholds for free shipping or bundling offers.
                                                                                                                                  
                                                                                                                                   16. ## Business Recommendations
                                                                                                                                  
                                                                                                                                   17. - Prioritize retention programs for top-decile customers identified by the top-customers analysis.
                                                                                                                                       - - Reallocate marketing spend toward categories with high profit margin, not just high revenue.
                                                                                                                                         - - Investigate regions with below-average profit margin for pricing, discounting, or cost issues.
                                                                                                                                           - - Use monthly trend and growth-rate outputs to inform inventory and staffing decisions ahead of peak months.
                                                                                                                                             - - Consider bundling or minimum-order incentives if the order-value distribution is heavily skewed toward small orders.
                                                                                                                                               - - Set up a recurring, for example monthly, run of this pipeline to keep KPIs and dashboards current.
                                                                                                                                                
                                                                                                                                                 - Manager Actions Checklist:
                                                                                                                                                 - - Review top 10 customers and assign account owners.
                                                                                                                                                   - - Review bottom-margin categories and products for pricing review.
                                                                                                                                                     - - Feed data/processed/cleaned_sales_data.csv into the BI tool of choice such as Power BI, Tableau, or Looker Studio.
                                                                                                                                                       - - Schedule a monthly re-run of the pipeline as new data arrives.
                                                                                                                                                        
                                                                                                                                                         - ## Executive Summary
                                                                                                                                                        
                                                                                                                                                         - This project delivers a reusable pipeline that turns raw retail sales exports into clean data, business KPIs, and decision-ready charts. It is designed so a non-technical stakeholder can run one command and receive a cleaned CSV for BI tools plus a folder of charts and summary tables covering revenue, profit, customers, products, and regions.
                                                                                                                                                        
                                                                                                                                                         - ## Future Improvements
                                                                                                                                                        
                                                                                                                                                         - - Add automated tests using pytest for the src modules.
                                                                                                                                                           - - Add a lightweight Streamlit or Dash dashboard on top of outputs.
                                                                                                                                                             - - Add SQL export scripts and a sample Power BI template.
                                                                                                                                                               - - Add continuous integration with GitHub Actions to lint and test on every push.
                                                                                                                                                                 - - Add anomaly detection for outlier orders.
                                                                                                                                                                  
                                                                                                                                                                   - ## License
                                                                                                                                                                  
                                                                                                                                                                   - This project is licensed under the MIT License. See the LICENSE file for details.
                                                                                                                                                                  
                                                                                                                                                                   - ## Author
                                                                                                                                                                  
                                                                                                                                                                   - Maintained as a data analytics portfolio project.
                                                                                                                                                                   - 
