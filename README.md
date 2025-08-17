# Sales Strategy Analysis for Pens & Printers Product Launch

## Business Overview

Pens & Printers recently launched a new product line using **three sales strategies**:  
- **Email**  
- **Call**  
- **Email + Call**  

With the upcoming launch of another product line, the **Business Intelligence team** was tasked to evaluate the effectiveness of these strategies. The objective is to determine which sales method(s) should be prioritized for maximizing **customer reach, revenue, and efficiency**.

This report outlines the **data validation process, exploratory analysis, business metrics, and recommendations** based on insights from the previous campaign.

---

## Dataset

- **Source**: Provided by DataCamp for educational purposes.  
- **File**: `product_sales.csv`  
- **Rows (before cleaning)**: 15,000  
- **Columns**: 8  
- **Disclaimer**: This dataset is **simulated** and not based on real company data.

---

## Tools Used

- **Python**  
- **Pandas** for data manipulation  
- **Matplotlib** & **Seaborn** for visualizations  
- **Jupyter Notebook** for analysis and documentation  

---

## Data Validation

The original dataset contained **15,000 rows and 8 columns**. A column-by-column validation was conducted:

- **`week`**: 6 unique values (`1–6`). No issues.  
- **`sales_method`**: Inconsistent entries cleaned → standardized to `Email`, `Call`, `Email + Call`.  
- **`customer_id`**: All unique. No issues.  
- **`nb_sold`**: Numeric, no missing values.  
- **`revenue`**: 1,074 missing → rows dropped.  
- **`years_as_customer`**: 2 invalid values (>41 years) → rows dropped.  
- **`nb_site_visits`**: Numeric, no missing values.  
- **`state`**: Consistent U.S. states, no missing values.  

### Final Dataset
- **Rows**: 13,924  
- **Columns**: 8  
- **Status**: Clean, validated, and ready for analysis.  

---

## Exploratory Analysis

### 1. Customer Reach by Sales Method
![customers_by_sales_method](customers_by_sales_method.png)

- **Email**: 6,921 customers — **widest reach** with minimal effort.  
- **Call**: 4,780 customers — **lower reach**, time-intensive.  
- **Email + Call**: 2,223 customers — **targeted approach**.  

---

### 2. Revenue Distribution (Overall and by Method)
![overall_revenue_spread-1](overall_revenue_spread-1.png)  
![revenue_spread_by_sales_method](revenue_spread_by_sales_method.png)

- **Email + Call**: **Highest median revenue** and **widest range**.  
- **Email**: Moderate performance with variability.  
- **Call**: Lowest performer but consistent.  

---

### 3. Revenue Over Time
![average_weekly_revenue_by_sales_method](average_weekly_revenue_by_sales_method.png)

- **Email + Call**: Consistently **top performer**.  
- **Email**: Strong start, then plateau.  
- **Call**: Steady but **lowest revenue overall**.  

---

## Business Metric: Average Revenue per Customer

![business_metric_average_revenue_per_customer](business_metric_average_revenue_per_customer.png)

| Sales Method     | Avg. Revenue per Customer |
| ---------------- | -------------------------- |
| **Email + Call** | 183.65                     |
| **Email**        | 97.13                      |
| **Call**         | 47.60                      |

- **Email + Call** shows the **highest return per customer**, justifying additional effort.  

---

## Future Customer Insights

Explored differences in **tenure, engagement, and location**, but results were **inconclusive**.  
Further segmentation is recommended using:  

- **Years as Customer**  
- **Website Visit Frequency**  
- **State / Region**  

This would allow **personalized sales strategies** and improve **targeting of high-value customers**.  

---

## Final Recommendations

- **Adopt "Email + Call"** for **high-value or strategic accounts**.  
- **Use Email-only** for **broad, scalable outreach**.  
- **Use Call-only** for **non-digital or unresponsive customers**.  
- **Track Average Revenue per Customer weekly** to monitor and refine strategy.  
- **Invest in customer segmentation** to uncover deeper patterns and optimize campaigns.  

---

## Key Takeaways

- **Email + Call** = Best overall strategy (high impact, high revenue).  
- **Email-only** = Cost-effective for mass outreach.  
- **Call-only** = Niche usage, not scalable.  

This analysis provides a **data-driven basis** for selecting the **right sales strategy** for the upcoming product launch.

---

## How to Reproduce

To reproduce this analysis on your machine:

```bash
# Clone this repository
git clone https://github.com/yourusername/pens-printers-sales-strategy.git
cd pens-printers-sales-strategy

# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the analysis
python run_analysis.py --input data/product_sales.csv --outdir figures
