# Data Cleaning Summary Report
## E-Commerce Sales Analysis Project — Week 6 Internship Assignment

**Generated:** October 27, 2026 at 16:31  
**Script:** `src/data_cleaning.py`  
**Input file:** `data/raw_sales_data.csv`  
**Output file:** `data/cleaned_sales.csv`

---

## 1. Dataset Overview (Before Cleaning)

| Metric | Value |
|--------|-------|
| Total Rows | 9,997 |
| Total Columns | 21 |
| Columns | Row ID, Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit |

## 2. Missing Value Analysis (Before Cleaning)

| Column | Missing Count | Missing % |
|--------|---------------|----------|
| Ship Date | 12 | 0.12% |

## 3. Duplicate Records (Before Cleaning)

| Metric | Value |
|--------|-------|
| Exact Duplicate Rows | 3 |

## 4. Cleaning Operations Performed

| # | Operation | Records Affected | Justification |
|---|-----------|------------------|---------------|
| 1 | Remove exact duplicate rows | 3 | Duplicate rows add bias to analysis |
| 2 | Retain NULL Ship Date records | 12 | Represent legitimate unshipped orders |
| 3 | Remove non-positive Sales records | 0 | Sales ≤ 0 indicate returns or errors |
| 4 | Remove non-positive Quantity records | 0 | Quantity ≤ 0 is physically invalid |
| 5 | Clip Discount to [0, 1] range | 0 | Discount > 100% or < 0% is invalid |
| 6 | Normalize string columns | All string cols | Ensure consistent category values |
| 7 | Parse date columns | Order Date, Ship Date | Enable temporal analysis |
| 8 | Add derived temporal features | All rows | Year, Month, Quarter for trend analysis |
| 9 | Add Profit Margin % column | All rows | Core KPI for business analysis |

## 5. Outlier Analysis

Outlier detection was performed using the **IQR method (1.5×IQR rule)**.

> **Decision:** Outliers in Sales and Profit are **retained** unless they represent  
> physically impossible values. In retail data, large bulk orders and promotional  
> sales legitimately produce extreme values. Removing them would distort analysis.

## 6. Dataset Summary (After Cleaning)

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total Rows | 9,997 | 9,994 | -3 |
| Total Columns | 21 | 26 | +5 (derived) |
| Missing Values | 12 | 12 | — |
| Duplicate Rows | 3 | 0 | -3 |

## 7. Cleaned Dataset Properties

| Property | Value |
|----------|-------|
| Date Range | 2020-01-01 to 2023-12-31 |
| Unique Orders | 9,070 |
| Unique Customers | 800 |
| Output File | `data/cleaned_sales.csv` |

## 8. Reproducibility

This cleaning process is fully reproducible:
- Fixed random seed where applicable
- All operations are deterministic
- No manual editing of individual records
- Raw dataset preserved at `data/raw_sales_data.csv`

## 9. Data Cleaning Log

```
[INFO] 16:31:05 | ============================================================
[INFO] 16:31:05 | E-COMMERCE SALES DATA CLEANING — WEEK 6 ASSIGNMENT
[INFO] 16:31:05 | ============================================================
[INFO] 16:31:05 | Loading dataset from: C:\Users\TUSHAR MARATHE\OneDrive\Documents\ai pROJECT\ecommerce-sales-analysis\data\raw_sales_data.csv
[INFO] 16:31:06 | Dataset loaded successfully. Shape: (9997, 21)
[INFO] 16:31:06 | === INITIAL INSPECTION ===
[INFO] 16:31:06 | Shape: 9,997 rows × 21 columns
[INFO] 16:31:06 | Columns: ['Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode', 'Customer ID', 'Customer Name', 'Segment', 'Country', 'City', 'State', 'Postal Code', 'Region', 'Product ID', 'Category', 'Sub-Category', 'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit']
[INFO] 16:31:06 | Memory usage: 9.12 MB
[INFO] 16:31:06 |   Column: 'Row ID' | dtype: int64
[INFO] 16:31:06 |   Column: 'Order ID' | dtype: str
[INFO] 16:31:06 |   Column: 'Order Date' | dtype: str
[INFO] 16:31:06 |   Column: 'Ship Date' | dtype: str
[INFO] 16:31:06 |   Column: 'Ship Mode' | dtype: str
[INFO] 16:31:06 |   Column: 'Customer ID' | dtype: str
[INFO] 16:31:06 |   Column: 'Customer Name' | dtype: str
[INFO] 16:31:06 |   Column: 'Segment' | dtype: str
[INFO] 16:31:06 |   Column: 'Country' | dtype: str
[INFO] 16:31:06 |   Column: 'City' | dtype: str
[INFO] 16:31:06 |   Column: 'State' | dtype: str
[INFO] 16:31:06 |   Column: 'Postal Code' | dtype: int64
[INFO] 16:31:06 |   Column: 'Region' | dtype: str
[INFO] 16:31:06 |   Column: 'Product ID' | dtype: str
[INFO] 16:31:06 |   Column: 'Category' | dtype: str
[INFO] 16:31:06 |   Column: 'Sub-Category' | dtype: str
[INFO] 16:31:06 |   Column: 'Product Name' | dtype: str
[INFO] 16:31:06 |   Column: 'Sales' | dtype: float64
[INFO] 16:31:06 |   Column: 'Quantity' | dtype: int64
[INFO] 16:31:06 |   Column: 'Discount' | dtype: float64
[INFO] 16:31:06 |   Column: 'Profit' | dtype: float64
[INFO] 16:31:06 | === MISSING VALUE ANALYSIS ===
[INFO] 16:31:06 |   'Ship Date': 12 missing (0.12%)
[INFO] 16:31:06 | === DUPLICATE DETECTION ===
[INFO] 16:31:06 | Exact duplicate rows found: 3
[INFO] 16:31:06 | === DATE PARSING AND VALIDATION ===
[INFO] 16:31:06 |   'Order Date' parsed with format '%d/%m/%Y'. Unparseable values: 0
[INFO] 16:31:06 |   'Ship Date' parsed with format '%d/%m/%Y'. Unparseable values: 0
[INFO] 16:31:06 |   Records where Ship Date < Order Date: 0
[INFO] 16:31:06 | === COLUMN TYPE IDENTIFICATION ===
[INFO] 16:31:06 |   Numerical columns (6): ['Row ID', 'Postal Code', 'Sales', 'Quantity', 'Discount', 'Profit']
[INFO] 16:31:06 |   Categorical columns (13): ['Order ID', 'Ship Mode', 'Customer ID', 'Customer Name', 'Segment', 'Country', 'City', 'State', 'Region', 'Product ID', 'Category', 'Sub-Category', 'Product Name']
[INFO] 16:31:06 |   Date columns (2): ['Order Date', 'Ship Date']
[INFO] 16:31:06 | === INVALID RECORD DETECTION ===
[INFO] 16:31:06 |   Records with Sales <= 0: 0
[INFO] 16:31:06 |   Records with Quantity <= 0: 0
[INFO] 16:31:06 |   Records with Discount outside [0, 1]: 0
[INFO] 16:31:06 |   Potential Profit outliers (±3×IQR): 1,733
[INFO] 16:31:06 | === CLEANING OPERATIONS ===
[INFO] 16:31:06 |   [CLEAN] Removed 3 exact duplicate rows.
[INFO] 16:31:06 |   [RETAIN] 12 records with NULL Ship Date retained (represent unshipped orders).
[INFO] 16:31:06 |   [CLEAN] Removed 0 records with Sales <= 0.
[INFO] 16:31:06 |   [CLEAN] Removed 0 records with Quantity <= 0.
[INFO] 16:31:06 |   [CLEAN] Clipped 0 Discount values to [0, 1] range.
[INFO] 16:31:06 |   [CLEAN] Stripped whitespace from string columns.
[INFO] 16:31:06 |   [ADD] Derived temporal features: Year, Month, Quarter.
[INFO] 16:31:06 |   [ADD] Derived feature: Profit Margin %
[INFO] 16:31:06 | === FINAL VALIDATION ===
[INFO] 16:31:06 |   Final shape: 9,994 rows × 26 columns
[INFO] 16:31:06 |   Remaining missing values: 12
[INFO] 16:31:06 |   Date range: 2020-01-01 to 2023-12-31
[INFO] 16:31:06 |   Sales range: $3.38 to $61198.74
[INFO] 16:31:06 |   Unique Order IDs: 9,070
[INFO] 16:31:06 |   Unique Customers: 800
[INFO] 16:31:06 |   Categories: ['Office Supplies', 'Furniture', 'Technology']
[INFO] 16:31:06 |   Regions: ['Central', 'East', 'West', 'South']
[INFO] 16:31:06 |   Segments: ['Home Office', 'Consumer', 'Corporate']
[INFO] 16:31:06 | 
[OK] Cleaned dataset saved to: C:\Users\TUSHAR MARATHE\OneDrive\Documents\ai pROJECT\ecommerce-sales-analysis\data\cleaned_sales.csv
[INFO] 16:31:06 | [OK] Cleaned dataset copy saved to: C:\Users\TUSHAR MARATHE\OneDrive\Documents\ai pROJECT\ecommerce-sales-analysis\data\processed\cleaned_sales.csv
```

---
*Report generated by `src/data_cleaning.py` — Week 6 Internship Assignment*
