import pandas as pd
from pens_printers_analysis import clean_data

def test_cleaning_pipeline_drops_null_revenue_and_bounds_years():
    df = pd.DataFrame({
        "sales_method": ["Email", "email", "em + call", "SMS"],
        "revenue": [10.0, None, 25.0, 5.0],
        "years_as_customer": [0, 10, 42, -1],
        "week": [1, 2, 3, 4],
    })
    cleaned = clean_data(df)
    # no null revenue
    assert cleaned["revenue"].isna().sum() == 0
    # methods standardized and filtered
    assert set(cleaned["sales_method"].unique()).issubset({"Email", "Call", "Email + Call"})
    # years bounded
    assert cleaned["years_as_customer"].between(0, 41).all()
