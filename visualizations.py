"""
visualizations.py
------------------
Generates key charts (matplotlib/seaborn) summarizing the EDA findings.
Saves PNGs into visuals/ for use in the README / portfolio.

Run:
    python src/visualizations.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 120

df = pd.read_csv("data/clean_sales_data.csv", parse_dates=["Order_Date"])
df["Year_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# 1. Revenue by Region
plt.figure(figsize=(8, 5))
regional = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
sns.barplot(x=regional.index, y=regional.values, hue=regional.index, legend=False)
plt.title("Total Sales by Region")
plt.ylabel("Sales (INR)")
plt.xlabel("Region")
plt.tight_layout()
plt.savefig("visuals/sales_by_region.png")
plt.close()

# 2. Profit Margin by Category
plt.figure(figsize=(8, 5))
cat = df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
cat["Margin_%"] = cat["Profit"] / cat["Sales"] * 100
cat = cat.sort_values("Margin_%", ascending=False)
sns.barplot(x=cat.index, y=cat["Margin_%"], hue=cat.index, legend=False)
plt.title("Profit Margin % by Product Category")
plt.ylabel("Profit Margin (%)")
plt.xlabel("Category")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("visuals/margin_by_category.png")
plt.close()

# 3. Monthly Sales Trend
plt.figure(figsize=(11, 5))
mom = df.groupby("Year_Month")["Sales"].sum()
plt.plot(mom.index, mom.values, marker="o", linewidth=2)
plt.title("Month-over-Month Sales Trend (2023-2024)")
plt.ylabel("Sales (INR)")
plt.xlabel("Month")
plt.xticks(rotation=75, fontsize=7)
plt.tight_layout()
plt.savefig("visuals/mom_sales_trend.png")
plt.close()

# 4. Customer Segment Revenue Share
plt.figure(figsize=(6, 6))
seg = df.groupby("Customer_Segment")["Sales"].sum()
plt.pie(seg.values, labels=seg.index, autopct="%1.1f%%", startangle=90,
        colors=sns.color_palette("viridis", len(seg)))
plt.title("Revenue Share by Customer Segment")
plt.tight_layout()
plt.savefig("visuals/customer_segment_share.png")
plt.close()

# 5. Sales Channel Performance
plt.figure(figsize=(8, 5))
channel = df.groupby("Sales_Channel")["Sales"].sum().sort_values(ascending=False)
sns.barplot(x=channel.index, y=channel.values, hue=channel.index, legend=False)
plt.title("Total Sales by Channel")
plt.ylabel("Sales (INR)")
plt.xlabel("Channel")
plt.tight_layout()
plt.savefig("visuals/sales_by_channel.png")
plt.close()

print("Saved 5 charts to visuals/")
