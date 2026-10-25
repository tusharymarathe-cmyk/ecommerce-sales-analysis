# Power BI DAX Measures
## E-Commerce Sales & Profitability Analytics Dashboard

**Table Name in Power BI:** `cleaned_sales` (rename if different)  
**Dataset:** `data/cleaned_sales.csv`

> **Important:** Replace `cleaned_sales` with the actual table name shown in your Power BI Fields pane. Column names must exactly match the CSV headers.

---

## Core KPI Measures

```dax
-- ============================================================
-- TOTAL SALES
-- Description: Sum of all transaction revenues
-- Format: Currency ($)
-- ============================================================
Total Sales = 
SUM('cleaned_sales'[Sales])


-- ============================================================
-- TOTAL PROFIT
-- Description: Sum of all transaction profits (can be negative)
-- Format: Currency ($)
-- ============================================================
Total Profit = 
SUM('cleaned_sales'[Profit])


-- ============================================================
-- TOTAL QUANTITY
-- Description: Total units sold across all transactions
-- Format: Whole number
-- ============================================================
Total Quantity = 
SUM('cleaned_sales'[Quantity])


-- ============================================================
-- TOTAL ORDERS
-- Description: Count of DISTINCT Order IDs
-- Note: Use DISTINCTCOUNT (not COUNT) to avoid double-counting
--       orders with multiple products
-- Format: Whole number
-- ============================================================
Total Orders = 
DISTINCTCOUNT('cleaned_sales'[Order ID])


-- ============================================================
-- TOTAL CUSTOMERS
-- Description: Count of unique customers
-- Format: Whole number
-- ============================================================
Total Customers = 
DISTINCTCOUNT('cleaned_sales'[Customer ID])


-- ============================================================
-- PROFIT MARGIN %
-- Description: Net profit as percentage of total sales
-- Note: Uses DIVIDE to safely handle division by zero
-- Format: Percentage (2 decimal places)
-- ============================================================
Profit Margin % = 
DIVIDE([Total Profit], [Total Sales], 0) * 100


-- ============================================================
-- AVERAGE ORDER VALUE
-- Description: Average revenue per unique order
-- Format: Currency ($)
-- ============================================================
Average Order Value = 
DIVIDE([Total Sales], [Total Orders], 0)


-- ============================================================
-- AVERAGE DISCOUNT RATE
-- Description: Average discount applied across all transactions
-- Format: Percentage
-- ============================================================
Average Discount = 
AVERAGE('cleaned_sales'[Discount]) * 100
```

---

## Time Intelligence Measures

```dax
-- ============================================================
-- YEAR-TO-DATE SALES
-- Description: Sales accumulated from the start of the year
-- Requires: Date table marked in Power BI
-- ============================================================
YTD Sales = 
TOTALYTD([Total Sales], 'cleaned_sales'[Order Date])


-- ============================================================
-- PRIOR YEAR SALES
-- Description: Total sales for the same period in the prior year
-- ============================================================
Prior Year Sales = 
CALCULATE([Total Sales], 
    DATEADD('cleaned_sales'[Order Date], -1, YEAR))


-- ============================================================
-- YEAR-OVER-YEAR GROWTH %
-- Description: Sales growth percentage vs prior year
-- Format: Percentage
-- ============================================================
YoY Sales Growth % = 
VAR CurrentSales = [Total Sales]
VAR PriorSales = [Prior Year Sales]
RETURN
DIVIDE(CurrentSales - PriorSales, PriorSales, 0) * 100


-- ============================================================
-- MONTHLY SALES (for trend chart)
-- ============================================================
Monthly Sales = 
CALCULATE([Total Sales],
    DATESMTD('cleaned_sales'[Order Date]))
```

---

## Segment and Category Measures

```dax
-- ============================================================
-- CONSUMER SALES
-- ============================================================
Consumer Sales = 
CALCULATE([Total Sales], 
    'cleaned_sales'[Segment] = "Consumer")


-- ============================================================
-- CORPORATE SALES
-- ============================================================
Corporate Sales = 
CALCULATE([Total Sales], 
    'cleaned_sales'[Segment] = "Corporate")


-- ============================================================
-- HOME OFFICE SALES
-- ============================================================
Home Office Sales = 
CALCULATE([Total Sales], 
    'cleaned_sales'[Segment] = "Home Office")


-- ============================================================
-- TECHNOLOGY PROFIT MARGIN
-- ============================================================
Technology Profit Margin % = 
CALCULATE([Profit Margin %],
    'cleaned_sales'[Category] = "Technology")


-- ============================================================
-- FURNITURE PROFIT MARGIN
-- ============================================================
Furniture Profit Margin % = 
CALCULATE([Profit Margin %],
    'cleaned_sales'[Category] = "Furniture")


-- ============================================================
-- OFFICE SUPPLIES PROFIT MARGIN
-- ============================================================
Office Supplies Profit Margin % = 
CALCULATE([Profit Margin %],
    'cleaned_sales'[Category] = "Office Supplies")
```

---

## Ranking Measures (for Top N Products)

```dax
-- ============================================================
-- PRODUCT SALES RANK
-- Description: Rank products by total sales (1 = highest)
-- Use in Table visual to show product rankings
-- ============================================================
Product Sales Rank = 
RANKX(
    ALL('cleaned_sales'[Product Name]),
    [Total Sales],
    ,
    DESC,
    Dense
)


-- ============================================================
-- IS TOP 10 PRODUCT
-- Description: Boolean filter to identify top 10 products
-- Use as a visual-level filter (= 1) on product charts
-- ============================================================
Is Top 10 Product = 
IF([Product Sales Rank] <= 10, 1, 0)
```

---

## Profitability Analysis Measures

```dax
-- ============================================================
-- LOSS-MAKING TRANSACTIONS
-- Description: Count of transactions with negative profit
-- ============================================================
Loss Transactions = 
CALCULATE(
    COUNTROWS('cleaned_sales'),
    'cleaned_sales'[Profit] < 0
)


-- ============================================================
-- PROFITABLE TRANSACTIONS
-- Description: Count of transactions with positive profit
-- ============================================================
Profitable Transactions = 
CALCULATE(
    COUNTROWS('cleaned_sales'),
    'cleaned_sales'[Profit] > 0
)


-- ============================================================
-- LOSS TRANSACTION RATE %
-- Description: Percentage of all transactions that are loss-making
-- ============================================================
Loss Rate % = 
DIVIDE([Loss Transactions], COUNTROWS('cleaned_sales'), 0) * 100


-- ============================================================
-- HIGH DISCOUNT SALES
-- Description: Sales at discount rate >= 20%
-- ============================================================
High Discount Sales = 
CALCULATE([Total Sales],
    'cleaned_sales'[Discount] >= 0.20)
```

---

## Formatting Recommendations

| Measure | Format String | Display Unit |
|---------|--------------|-------------|
| Total Sales | `$#,##0.00` | Thousands or Millions |
| Total Profit | `$#,##0.00` | Thousands |
| Total Orders | `#,##0` | None |
| Profit Margin % | `0.00\%` | None |
| Average Order Value | `$#,##0.00` | None |
| YoY Sales Growth % | `+0.00\%;-0.00\%` | None |

---

## Table Name Verification

If your table is named differently in Power BI:
1. Go to **Model View** in Power BI Desktop
2. Click on the table — the name appears in the Properties pane
3. Replace all instances of `'cleaned_sales'` in the DAX formulas with your actual table name

---

*DAX measures document created for Week 6 Internship Assignment — Power BI section*
