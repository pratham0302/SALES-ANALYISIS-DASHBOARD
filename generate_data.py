"""
generate_data.py
-----------------
Generates a realistic e-commerce transactional dataset (10,000+ rows)
with intentional data-quality issues (missing values, duplicates,
outliers, mixed types) so the cleaning pipeline has real work to do.

Run:
    python src/generate_data.py
Output:
    data/raw_sales_data.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

N_ROWS = 10500

REGIONS = ["North", "South", "East", "West", "Central"]
CATEGORIES = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Tablet"],
    "Furniture": ["Office Chair", "Study Table", "Bookshelf", "Sofa", "Bed Frame"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Kurta"],
    "Grocery": ["Rice 5kg", "Cooking Oil", "Snacks Pack", "Tea Powder", "Spices Combo"],
    "Beauty & Personal Care": ["Face Wash", "Shampoo", "Perfume", "Skincare Kit", "Trimmer"],
}
CHANNELS = ["Online", "In-Store", "Mobile App", "Marketplace"]
SEGMENTS = ["New", "Recurring", "VIP"]

# unit price ranges per category (min, max)
PRICE_RANGE = {
    "Electronics": (999, 65000),
    "Furniture": (1499, 25000),
    "Clothing": (299, 3999),
    "Grocery": (49, 999),
    "Beauty & Personal Care": (99, 2499),
}

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

# Create a pool of ~2500 recurring customer IDs so some customers repeat (needed for cohort/churn analysis)
customer_pool = [f"CUST{str(i).zfill(5)}" for i in range(1, 2501)]

rows = []
for i in range(1, N_ROWS + 1):
    order_id = f"ORD{100000 + i}"
    order_date = start_date + timedelta(days=random.randint(0, date_range_days))
    customer_id = random.choice(customer_pool)
    region = random.choice(REGIONS)
    category = random.choice(list(CATEGORIES.keys()))
    product = random.choice(CATEGORIES[category])
    quantity = random.randint(1, 6)
    low, high = PRICE_RANGE[category]
    unit_price = round(random.uniform(low, high), 2)

    # Regional discount skew: North & Central get higher discounts (mirrors resume claim)
    if region in ["North", "Central"]:
        discount = round(random.choice([0, 0, 0.05, 0.10, 0.15, 0.20, 0.25]), 2)
    else:
        discount = round(random.choice([0, 0, 0, 0.05, 0.10, 0.15]), 2)

    gross_sales = round(unit_price * quantity, 2)
    sales = round(gross_sales * (1 - discount), 2)

    # Margins vary by category (Electronics & Beauty = high margin, Grocery = low margin)
    margin_map = {
        "Electronics": 0.28, "Furniture": 0.22, "Clothing": 0.35,
        "Grocery": 0.08, "Beauty & Personal Care": 0.32,
    }
    base_margin = margin_map[category]
    profit = round(sales * (base_margin + random.uniform(-0.05, 0.05)), 2)

    channel = random.choice(CHANNELS)
    segment = random.choices(SEGMENTS, weights=[0.4, 0.45, 0.15])[0]

    rows.append([
        order_id, order_date.strftime("%Y-%m-%d"), customer_id, region,
        category, product, quantity, unit_price, discount, sales,
        profit, channel, segment
    ])

df = pd.DataFrame(rows, columns=[
    "Order_ID", "Order_Date", "Customer_ID", "Region", "Category",
    "Product_Name", "Quantity", "Unit_Price", "Discount", "Sales",
    "Profit", "Sales_Channel", "Customer_Segment"
])

# ---- Inject realistic data-quality issues ----

# 1. Missing values (~3% of Discount, ~2% of Sales_Channel, ~1.5% of Region)
for col, frac in [("Discount", 0.03), ("Sales_Channel", 0.02), ("Region", 0.015)]:
    idx = df.sample(frac=frac, random_state=1).index
    df.loc[idx, col] = np.nan

# 2. Duplicate rows (~1.5% duplicated order entries, simulating double-logging)
dupes = df.sample(frac=0.015, random_state=2)
df = pd.concat([df, dupes], ignore_index=True)

# 3. Outliers in Quantity and Unit_Price (data entry errors)
outlier_idx = df.sample(n=40, random_state=3).index
df.loc[outlier_idx[:20], "Quantity"] = df.loc[outlier_idx[:20], "Quantity"] * 50
df.loc[outlier_idx[20:], "Unit_Price"] = df.loc[outlier_idx[20:], "Unit_Price"] * 15

# 4. Mixed/dirty types in Discount (some stored as string with '%')
df["Discount"] = df["Discount"].astype(object)
str_idx = df.sample(frac=0.01, random_state=4).index
df.loc[str_idx, "Discount"] = df.loc[str_idx, "Discount"].apply(
    lambda x: f"{int(x*100)}%" if pd.notna(x) else x
)

# 5. Inconsistent region casing/whitespace (real-world messiness)
case_idx = df.sample(frac=0.01, random_state=5).index
df.loc[case_idx, "Region"] = df.loc[case_idx, "Region"].apply(
    lambda x: f" {x.lower()} " if pd.notna(x) else x
)

df.to_csv("data/raw_sales_data.csv", index=False)
print(f"Generated {len(df)} rows -> data/raw_sales_data.csv")
