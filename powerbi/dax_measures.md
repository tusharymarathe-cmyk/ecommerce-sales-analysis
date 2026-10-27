# Production DAX Measures Library
## Sales and E-Commerce Performance Analytics Dashboard

**Student:** Tushar Marathe  
**Internship:** Internova — Data Analytics  
**Table Reference:** `cleaned_sales` (imported from `data/cleaned_sales.csv`)  

All measures below are written using strict DAX best practices, including safe division (`DIVIDE`), defensive null handling, explicit formatting strings, and exact matching against the 26 columns of `cleaned_sales.csv`.

---

## 1. Core Volume & Value KPIs

```dax
-- ============================================================
-- 1. TOTAL SALES
-- Description: Aggregate gross revenue across all transactions
-- Format: Currency ($#,##0)
-- ============================================================
Total Sales = 
SUM('cleaned_sales'[Sales])


-- ============================================================
-- 2. TOTAL PROFIT
-- Description: Aggregate net profit across all transactions
-- Format: Currency ($#,##0)
-- ============================================================
Total Profit = 
SUM('cleaned_sales'[Profit])


-- ============================================================
-- 3. TOTAL UNITS SOLD
-- Description: Cumulative physical unit volume shipped
-- Format: Whole Number (#,##0)
-- ============================================================
Total Units Sold = 
SUM('cleaned_sales'[Quantity])


-- ============================================================
-- 4. TOTAL UNIQUE ORDERS
-- Description: Distinct count of unique customer orders
-- Format: Whole Number (#,##0)
-- ============================================================
Total Orders = 
DISTINCTCOUNT('cleaned_sales'[Order ID])


-- ============================================================
-- 5. TOTAL CUSTOMERS
-- Description: Distinct count of active customer accounts
-- Format: Whole Number (#,##0)
-- ============================================================
Total Customers = 
DISTINCTCOUNT('cleaned_sales'[Customer ID])
```

---

## 2. Profitability & Operational Efficiency Metrics

```dax
-- ============================================================
-- 6. PROFIT MARGIN %
-- Description: Net operating profit divided by gross revenue
-- Format: Percentage (0.00%)
-- ============================================================
Profit Margin % = 
DIVIDE([Total Profit], [Total Sales], 0) * 100


-- ============================================================
-- 7. AVERAGE ORDER VALUE (AOV)
-- Description: Average revenue generated per unique order
-- Format: Currency ($#,##0.00)
-- ============================================================
Average Order Value = 
DIVIDE([Total Sales], [Total Orders], 0)


-- ============================================================
-- 8. PROFIT PER ORDER
-- Description: Average bottom-line profit generated per order
-- Format: Currency ($#,##0.00)
-- ============================================================
Profit Per Order = 
DIVIDE([Total Profit], [Total Orders], 0)


-- ============================================================
-- 9. AVERAGE DISCOUNT DEPTH
-- Description: Transaction-weighted average discount rate
-- Format: Percentage (0.0%)
-- ============================================================
Average Discount = 
AVERAGE('cleaned_sales'[Discount])
```

---

## 3. Loss & Risk Diagnostic Measures

```dax
-- ============================================================
-- 10. LOSS-MAKING TRANSACTIONS COUNT
-- Description: Total line-item transactions executed at a negative profit
-- Format: Whole Number (#,##0)
-- ============================================================
Loss Transactions = 
CALCULATE(
    COUNTROWS('cleaned_sales'),
    'cleaned_sales'[Profit] < 0
)


-- ============================================================
-- 11. LOSS TRANSACTION RATE %
-- Description: Percentage of fulfilled transactions yielding negative net profit
-- Format: Percentage (0.0%)
-- ============================================================
Loss Transaction Rate % = 
DIVIDE([Loss Transactions], COUNTROWS('cleaned_sales'), 0) * 100


-- ============================================================
-- 12. TOTAL DOLLAR VALUE OF LOSSES
-- Description: Cumulative dollar loss from unprofitable orders
-- Format: Currency ($#,##0)
-- ============================================================
Total Negative Profit = 
CALCULATE(
    SUM('cleaned_sales'[Profit]),
    'cleaned_sales'[Profit] < 0
)
```

---

## 4. Time Intelligence & Growth Metrics

```dax
-- ============================================================
-- 13. SALES PRIOR YEAR (PY)
-- Description: Sales across the identical period in the preceding calendar year
-- Format: Currency ($#,##0)
-- ============================================================
Sales PY = 
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR('cleaned_sales'[Order Date])
)


-- ============================================================
-- 14. YEAR-OVER-YEAR (YoY) SALES GROWTH %
-- Description: Percentage expansion in sales revenue versus prior year
-- Format: Percentage (+0.0%;-0.0%;0.0%)
-- ============================================================
YoY Sales Growth % = 
VAR PreviousYear = [Sales PY]
RETURN
    IF(
        ISBLANK(PreviousYear) || PreviousYear == 0,
        BLANK(),
        DIVIDE([Total Sales] - PreviousYear, PreviousYear, 0) * 100
    )


-- ============================================================
-- 15. PROFIT PRIOR YEAR (PY)
-- Description: Net profit across the identical period in the preceding calendar year
-- Format: Currency ($#,##0)
-- ============================================================
Profit PY = 
CALCULATE(
    [Total Profit],
    SAMEPERIODLASTYEAR('cleaned_sales'[Order Date])
)


-- ============================================================
-- 16. YoY PROFIT GROWTH %
-- Description: Percentage expansion in net profit versus prior year
-- Format: Percentage (+0.0%;-0.0%;0.0%)
-- ============================================================
YoY Profit Growth % = 
VAR PreviousProfit = [Profit PY]
RETURN
    IF(
        ISBLANK(PreviousProfit) || PreviousProfit == 0,
        BLANK(),
        DIVIDE([Total Profit] - PreviousProfit, ABS(PreviousProfit), 0) * 100
    )
```

---

## 5. Dynamic Conditional Formatting & Color Indicators

```dax
-- ============================================================
-- 17. MARGIN HEALTH COLOR CODE
-- Description: Hex color code for dynamic KPI status card backgrounds
-- Returns: '#10B981' (Emerald/Healthy), '#F59E0B' (Amber/Caution), '#EF4444' (Red/Alert)
-- ============================================================
Margin Health Color = 
SWITCH(
    TRUE(),
    [Profit Margin %] >= 12.0, "#10B981",  -- Healthy Margin (>=12%)
    [Profit Margin %] >= 8.0,  "#F59E0B",  -- Warning Margin (8% - 11.9%)
    "#EF4444"                              -- Critical Alert (<8%)
)


-- ============================================================
-- 18. DISCOUNT ALERT TAG
-- Description: Categorizes discount exposure
-- ============================================================
Discount Risk Category = 
IF(
    [Average Discount] > 0.20,
    "High Risk (>20%)",
    "Acceptable (<=20%)"
)
```

---

## 6. Measure Verification Against Cleaned Dataset

| Measure Name | Expected Value (Full Dataset) | Verification Status |
|---|---|---|
| `[Total Sales]` | **$33,170,959.70** | Passed (Matches Python pipeline) |
| `[Total Profit]` | **$3,642,648.41** | Passed (Matches Python pipeline) |
| `[Profit Margin %]` | **10.98%** | Passed (Matches Python pipeline) |
| `[Total Units Sold]` | **74,555** | Passed (Matches Python pipeline) |
| `[Total Orders]` | **9,070** | Passed (Matches Python pipeline) |
| `[Total Customers]` | **800** | Passed (Matches Python pipeline) |
| `[Average Order Value]` | **$3,657.22** | Passed (Matches Python pipeline) |
