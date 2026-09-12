# Sales Data Analytics & Executive BI Dashboard

End-to-end e-commerce sales analytics project: from a raw, messy 10,000+
transaction dataset to an automated cleaning pipeline, statistical EDA,
and an executive Power BI dashboard with custom DAX measures.

## Tech Stack
`Python` · `Pandas` · `NumPy` · `Seaborn` · `Matplotlib` · `Power BI` · `DAX`

## Project Highlights

- **End-to-End EDA & Insight Mining** — Explored a 10,500-row e-commerce
  transaction dataset and identified 3 key revenue drivers: regional
  discount patterns, recurring/VIP customer value, and high-margin
  product categories.
- **Automated Data Wrangling Pipeline** — Missing value imputation,
  duplicate resolution, outlier mitigation (IQR capping), and dynamic
  type casting (e.g. `"15%"` strings → `0.15` floats), all logged with
  before/after row counts.
- **Statistical & Cohort Analysis** — Month-over-month sales velocity and
  customer cohort/retention analysis to guide inventory and discount
  strategy.
- **Executive Power BI Dashboard** — Multi-page report with custom DAX
  measures (YTD Sales, Profit Margin %, Customer Lifetime Value) and
  synchronized slicers for region/category/channel drill-downs.

## Repository Structure

```
sales-analytics-dashboard/
├── data/
│   ├── raw_sales_data.csv          # Generated raw data (with intentional messiness)
│   ├── clean_sales_data.csv        # Output of the cleaning pipeline
│   └── insight_*.csv               # Pre-aggregated tables for Power BI
├── src/
│   ├── generate_data.py            # Synthetic dataset generator
│   ├── data_cleaning.py            # Cleaning / wrangling pipeline
│   ├── eda_analysis.py             # EDA + insight mining
│   └── visualizations.py           # Chart generation (matplotlib/seaborn)
├── visuals/                        # Saved chart PNGs
├── powerbi/
│   └── DAX_measures.md             # DAX formulas + Power BI setup guide
├── requirements.txt
└── README.md
```

## How to Run

```bash
git clone https://github.com/<your-username>/sales-analytics-dashboard.git
cd sales-analytics-dashboard
pip install -r requirements.txt

# 1. Generate the raw dataset
python src/generate_data.py

# 2. Run the cleaning pipeline
python src/data_cleaning.py

# 3. Run EDA and export insight tables
python src/eda_analysis.py

# 4. Generate charts
python src/visualizations.py
```

Then open Power BI Desktop and follow `powerbi/DAX_measures.md` to load
`data/clean_sales_data.csv` and build the dashboard.

## Sample Results

| Metric | Value |
|---|---|
| Total transactions analyzed | 10,500 (post-cleaning) |
| Duplicate records removed | 158 |
| Outliers capped (IQR method) | 1,016 |
| Repeat purchase rate | ~94% |
| Recurring + VIP revenue share | ~60% |
| Highest-margin category | Electronics (28% margin) |

### Charts

![Sales by Region](visuals/sales_by_region.png)
![Margin by Category](visuals/margin_by_category.png)
![MoM Sales Trend](visuals/mom_sales_trend.png)

## Author

**Sharvan Kumar**
B.Tech CSE (3rd Year), Rungta College of Engineering and Technology
[GitHub](https://github.com/sharvan2357) · [LinkedIn](https://linkedin.com/in/sharvan-kumar)
