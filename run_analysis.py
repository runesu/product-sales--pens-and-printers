#!/usr/bin/env python3
import argparse
from pens_printers_analysis import (
    load_data,
    clean_data,
    eda_plots,
    business_metric_plot,
    print_brief_info,
)

def main():
    parser = argparse.ArgumentParser(
        description="Pens & Printers sales analysis"
    )
    parser.add_argument("--input", required=True, help="Path to product_sales.csv")
    parser.add_argument("--outdir", default="figures", help="Directory to save figures")
    parser.add_argument("--show", action="store_true", help="Show plots interactively")
    args = parser.parse_args()

    df = load_data(args.input)
    print_brief_info(df, note="Before cleaning")

    df_clean = clean_data(df)
    print_brief_info(df_clean, note="After cleaning")

    eda_plots(df_clean, outdir=args.outdir, show=args.show)
    business_metric_plot(df_clean, outdir=args.outdir, show=args.show)

if __name__ == "__main__":
    main()
