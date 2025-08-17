# Pens & Printers — Sales Strategy Analysis

Reusable code to load, clean, and analyze the `product_sales.csv` dataset for the Pens & Printers case study.

## What it does
- Loads CSV and inspects schema
- Cleans:
  - drops rows with missing `revenue` (1074 rows expected)
  - standardizes `sales_method` to one of: `Email`, `Call`, `Email + Call`
  - filters `years_as_customer` to [0, 41] (removes 2 rows expected)
- Produces EDA charts:
  - Customer count by sales method
  - Revenue distribution (overall + by method)
  - Average weekly revenue by method
  - Average revenue per customer per method (business metric)

## Quick start
```bash
//run the below commands within your project environment
python -m venv venv
venv\Scripts\activate    //activating for windows

pip install -r requirements.txt

# Run the following to run the analysis
python run_analysis.py --input data/product_sales.csv --outdir figures
