# Power BI Dashboard — DAX Measures & Setup Guide

This folder documents the DAX measures and data model used to build the
executive dashboard shown in the resume (multi-page report with synchronized
slicers for region, category, and sales channel drill-downs).

## 1. Load the data

1. Open Power BI Desktop → **Get Data → Text/CSV**
2. Load `data/clean_sales_data.csv` as the main fact table (`Sales`)
3. Optionally load the pre-aggregated insight CSVs from `data/` as
   supporting tables, or build everything straight from the fact table
   using the measures below.
4. Create a **Date table** (Modeling → New Table):

```DAX
DateTable =
CALENDAR(MIN(Sales[Order_Date]), MAX(Sales[Order_Date]))
```
Mark it as a Date Table (Modeling → Mark as Date Table), and relate
`DateTable[Date]` (1) → `Sales[Order_Date]` (many).

## 2. Core DAX Measures

```DAX
Total Sales = SUM(Sales[Sales])

Total Profit = SUM(Sales[Profit])

Profit Margin % =
DIVIDE([Total Profit], [Total Sales], 0)

Total Orders = DISTINCTCOUNT(Sales[Order_ID])

Avg Order Value = DIVIDE([Total Sales], [Total Orders], 0)

Unique Customers = DISTINCTCOUNT(Sales[Customer_ID])
```

## 3. Time-Intelligence Measures (YTD, MoM)

```DAX
YTD Sales =
TOTALYTD([Total Sales], DateTable[Date])

Sales LM =                 -- Sales, Last Month
CALCULATE([Total Sales], DATEADD(DateTable[Date], -1, MONTH))

MoM Growth % =
DIVIDE([Total Sales] - [Sales LM], [Sales LM], 0)

Sales SPLY =                -- Same Period Last Year
CALCULATE([Total Sales], SAMEPERIODLASTYEAR(DateTable[Date]))

YoY Growth % =
DIVIDE([Total Sales] - [Sales SPLY], [Sales SPLY], 0)
```

## 4. Customer Lifetime Value (CLV)

```DAX
Customer Lifetime Value =
DIVIDE([Total Sales], [Unique Customers], 0)

Repeat Customer Rate =
VAR CustomersWithMultipleOrders =
    COUNTROWS(
        FILTER(
            VALUES(Sales[Customer_ID]),
            CALCULATE([Total Orders]) > 1
        )
    )
RETURN
DIVIDE(CustomersWithMultipleOrders, [Unique Customers], 0)
```

## 5. Recommended Report Pages

| Page | Visuals | Slicers |
|---|---|---|
| **Executive Overview** | KPI cards (Total Sales, Profit, Margin %, YTD Sales), MoM trend line chart | Region, Date range |
| **Regional Performance** | Map/bar chart of Sales by Region, Discount vs Margin scatter | Region, Category |
| **Category & Product** | Treemap of Sales by Category, table of top products by profit | Category, Sales Channel |
| **Customer Insights** | Segment pie chart, CLV card, repeat-rate gauge | Customer Segment |

## 6. Slicer Sync

Use **View → Sync Slicers** to sync the Region, Category, and Sales Channel
slicers across all report pages so filtering on one page updates the others.

## 7. Files to import

- `data/clean_sales_data.csv` — main fact table
- `data/insight_regional_discounts.csv`
- `data/insight_customer_segments.csv`
- `data/insight_category_margins.csv`
- `data/insight_mom_trend.csv`
- `data/insight_cohort_analysis.csv`
