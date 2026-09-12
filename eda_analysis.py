"""
eda_analysis.py
----------------
Exploratory Data Analysis + insight mining on the cleaned sales dataset.
Surfaces the 3 revenue drivers referenced in the project summary:
  1. Regional discount impact
  2. Recurring customer segment value
  3. High-margin product categories
Also runs MoM trend and cohort/churn analysis.

Run:
    python src/eda_analysis.py
Input:
    data/clean_sales_data.csv
Output:
    Printed summary stats + CSV exports in data/ for Power BI
"""

import pandas as pd
import numpy as np

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

df = pd.read_csv("data/clean_sales_data.csv", parse_dates=["Order_Date"])
df["Year_Month"] = df["Order_Date"].dt.to_period("M")

print("=" * 60)
print("1. REGIONAL DISCOUNT IMPACT")
print("=" * 60)
regional = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Avg_Discount=("Discount", "mean"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order_ID", "count"),
).sort_values("Total_Sales", ascending=False)
regional["Profit_Margin_%"] = (regional["Total_Profit"] / regional["Total_Sales"] * 100).round(2)
print(regional)
regional.to_csv("data/insight_regional_discounts.csv")

print("\n" + "=" * 60)
print("2. RECURRING CUSTOMER SEGMENT VALUE")
print("=" * 60)
segment = df.groupby("Customer_Segment").agg(
    Total_Sales=("Sales", "sum"),
    Avg_Order_Value=("Sales", "mean"),
    Orders=("Order_ID", "count"),
    Unique_Customers=("Customer_ID", "nunique"),
).sort_values("Total_Sales", ascending=False)
segment["Revenue_Share_%"] = (segment["Total_Sales"] / segment["Total_Sales"].sum() * 100).round(2)
print(segment)
segment.to_csv("data/insight_customer_segments.csv")

# Repeat purchase rate
order_counts = df.groupby("Customer_ID")["Order_ID"].count()
repeat_rate = (order_counts > 1).mean() * 100
print(f"\nRepeat purchase rate: {repeat_rate:.2f}% of customers ordered more than once")

print("\n" + "=" * 60)
print("3. HIGH-MARGIN PRODUCT CATEGORIES")
print("=" * 60)
category = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Orders=("Order_ID", "count"),
).sort_values("Total_Profit", ascending=False)
category["Profit_Margin_%"] = (category["Total_Profit"] / category["Total_Sales"] * 100).round(2)
print(category)
category.to_csv("data/insight_category_margins.csv")

print("\n" + "=" * 60)
print("4. MONTH-OVER-MONTH (MoM) SALES VELOCITY")
print("=" * 60)
mom = df.groupby("Year_Month")["Sales"].sum().reset_index()
mom["Sales"] = mom["Sales"].round(2)
mom["MoM_Growth_%"] = mom["Sales"].pct_change().mul(100).round(2)
print(mom.to_string(index=False))
mom.to_csv("data/insight_mom_trend.csv", index=False)

print("\n" + "=" * 60)
print("5. COHORT ANALYSIS - CUSTOMER FIRST PURCHASE MONTH")
print("=" * 60)
first_purchase = df.groupby("Customer_ID")["Order_Date"].min().dt.to_period("M")
df["Cohort_Month"] = df["Customer_ID"].map(first_purchase)
df["Order_Period_Number"] = (
    (df["Year_Month"] - df["Cohort_Month"]).apply(lambda x: x.n)
)
cohort_pivot = df.pivot_table(
    index="Cohort_Month", columns="Order_Period_Number",
    values="Customer_ID", aggfunc="nunique"
)
cohort_pivot.to_csv("data/insight_cohort_analysis.csv")
print(f"Cohort matrix saved -> data/insight_cohort_analysis.csv "
      f"({cohort_pivot.shape[0]} cohorts x {cohort_pivot.shape[1]} periods)")

print("\n" + "=" * 60)
print("SUMMARY: KEY TAKEAWAYS")
print("=" * 60)
top_region = regional["Total_Sales"].idxmax()
top_category = category["Total_Profit"].idxmax()
print(f"- Highest revenue region: {top_region}")
print(f"- Highest profit-margin category: {top_category}")
print(f"- Recurring + VIP customers contribute "
      f"{segment.loc[['Recurring','VIP'], 'Revenue_Share_%'].sum():.2f}% of total revenue")
print(f"- Overall repeat purchase rate: {repeat_rate:.2f}%")
