# Processed Data

This folder receives the cleaned dataset produced by running the pipeline:

```bash
python -m src.main --input data/raw/sample_sales_data.csv
```

The output file cleaned_sales_data.csv will contain the cleaned, feature-engineered dataset (missing values handled, duplicates removed, outliers capped, and additional columns such as order_month and profit_margin). This folder is empty until you run the pipeline.
