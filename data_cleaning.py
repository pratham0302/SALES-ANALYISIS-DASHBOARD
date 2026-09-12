"""
data_cleaning.py
-----------------
Automated data wrangling pipeline:
- Duplicate resolution
- Missing value imputation
- Outlier mitigation (IQR method)
- Dynamic type casting (e.g. "15%" strings -> float)
- Text normalization (casing/whitespace)

Run:
    python src/data_cleaning.py
Input:
    data/raw_sales_data.csv
Output:
    data/clean_sales_data.csv
"""

import pandas as pd
import numpy as np
import time

RAW_PATH = "data/raw_sales_data.csv"
CLEAN_PATH = "data/clean_sales_data.csv"


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def normalize_region(df: pd.DataFrame) -> pd.DataFrame:
    df["Region"] = df["Region"].astype(str).str.strip().str.title()
    df["Region"] = df["Region"].replace("Nan", np.nan)
    return df


def fix_discount_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert string percentages like '15%' into floats (0.15)."""
    def parse_discount(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, str) and "%" in val:
            return round(float(val.strip("%")) / 100, 2)
        return float(val)

    df["Discount"] = df["Discount"].apply(parse_discount)
    return df


def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    # Discount: impute with median discount per Category
    df["Discount"] = df.groupby("Category")["Discount"].transform(
        lambda s: s.fillna(s.median())
    )
    # Sales_Channel: impute with mode
    df["Sales_Channel"] = df["Sales_Channel"].fillna(df["Sales_Channel"].mode()[0])
    # Region: impute with mode (rare case)
    df["Region"] = df["Region"].fillna(df["Region"].mode()[0])
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates(subset=["Order_ID"], keep="first")
    removed = before - len(df)
    print(f"Removed {removed} duplicate order records")
    return df


def mitigate_outliers(df: pd.DataFrame, cols=("Quantity", "Unit_Price")) -> pd.DataFrame:
    """Cap outliers using the IQR method instead of dropping rows (preserves sample size)."""
    for col in cols:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_outliers = ((df[col] < lower) | (df[col] > upper)).sum()
        df[col] = df[col].clip(lower=lower, upper=upper)
        print(f"Capped {n_outliers} outliers in '{col}' (bounds: {lower:.2f} - {upper:.2f})")
    return df


def recompute_derived_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Recompute Sales/Profit after outlier capping so totals stay internally consistent."""
    df["Sales"] = (df["Unit_Price"] * df["Quantity"] * (1 - df["Discount"])).round(2)
    margin_map = {
        "Electronics": 0.28, "Furniture": 0.22, "Clothing": 0.35,
        "Grocery": 0.08, "Beauty & Personal Care": 0.32,
    }
    df["Profit"] = df.apply(
        lambda r: round(r["Sales"] * margin_map.get(r["Category"], 0.2), 2), axis=1
    )
    return df


def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Quantity"] = df["Quantity"].astype(int)
    for col in ["Unit_Price", "Discount", "Sales", "Profit"]:
        df[col] = df[col].astype(float)
    return df


def run_pipeline():
    t0 = time.time()
    df = load_data(RAW_PATH)
    print(f"Loaded {len(df)} raw rows")

    df = normalize_region(df)
    df = fix_discount_types(df)
    df = remove_duplicates(df)
    df = impute_missing(df)
    df = mitigate_outliers(df)
    df = recompute_derived_fields(df)
    df = cast_types(df)

    df.to_csv(CLEAN_PATH, index=False)
    elapsed = time.time() - t0
    print(f"\nClean dataset saved: {CLEAN_PATH}")
    print(f"Final row count: {len(df)}")
    print(f"Pipeline runtime: {elapsed:.2f}s")
    print(f"Remaining nulls:\n{df.isna().sum()[df.isna().sum() > 0]}")


if __name__ == "__main__":
    run_pipeline()
