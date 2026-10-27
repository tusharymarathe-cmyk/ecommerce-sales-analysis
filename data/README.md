# Data Directory — Sales and E-Commerce Performance Analytics

**Student:** Tushar Marathe | **Organization:** Internova | **Domain:** Data Analytics  
**Assignment:** Week 6 Final Project  

---

## 1. Directory Overview & Structure

This directory houses the raw and processed e-commerce transaction datasets used across the Python analytics pipeline, Jupyter Notebooks, and Power BI dashboard.

```text
data/
├── README.md                   # This data dictionary and provenance guide
├── raw/
│   └── raw_sales_data.csv      # Raw ingested dataset (9,997 rows, 21 columns)
├── processed/
│   └── cleaned_sales.csv       # Cleaned, validated & feature-engineered dataset (9,994 rows, 26 columns)
├── raw_sales_data.csv          # Root compatibility mirror of raw dataset
└── cleaned_sales.csv           # Root compatibility mirror of processed dataset
```

---

## 2. Dataset Provenance, Methodology & Disclosure

> **Transparency Disclosure:**  
> The dataset analyzed in this project is synthetically generated using calibrated statistical parameters modeled after the public Tableau Sample Superstore schema (`numpy.random.seed(42)`).  
> All business metrics, KPIs, regional breakdowns, and recommendations are derived directly from this dataset for academic evaluation.

### Generation & Calibration Parameters:
- **Temporal Coverage:** January 1, 2020 through December 31, 2023 (4 Full Operating Years).
- **Categories:** Technology (34%), Office Supplies (33%), Furniture (33%).
- **Geographic Territories:** West (30%), East (28%), Central (22%), South (20%).
- **Customer Base:** 800 distinct customer accounts across Consumer (52%), Corporate (30%), and Home Office (18%) segments.
- **Controlled Data Anomalies:** 3 duplicate rows injected; 12 null `Ship Date` entries representing pending orders.

---

## 3. Schema & Feature Definitions

### Core Business Features (21 Raw Features)

| Column Name | Data Type | Business Description | Valid Range / Example |
|---|---|---|---|
| `Row ID` | Integer | Unique transaction row identifier | 1 to 9,997 |
| `Order ID` | String | Unique purchase order code | `CA-2022-152156` |
| `Order Date` | Datetime | Date customer placed the order | `2020-01-01` to `2023-12-31` |
| `Ship Date` | Datetime | Date order was dispatched | `2020-01-03` to `2024-01-05` (or NULL) |
| `Ship Mode` | String | Logistics shipping service tier | `Standard Class`, `Second Class`, `First Class`, `Same Day` |
| `Customer ID` | String | Unique customer identifier | `CUST-00001` to `CUST-00800` |
| `Customer Name` | String | Customer full name | Text |
| `Segment` | String | Customer market classification | `Consumer`, `Corporate`, `Home Office` |
| `Country` | String | Operational country | `United States` |
| `City` | String | Destination delivery city | Text (e.g., New York, Los Angeles) |
| `State` | String | Destination state / province | Text |
| `Postal Code` | Integer | Delivery ZIP code | 5-digit postal code |
| `Region` | String | Sales management territory | `West`, `East`, `Central`, `South` |
| `Product ID` | String | Unique stock keeping unit (SKU) | `Prod-TEC-COP-0001` |
| `Category` | String | High-level product classification | `Technology`, `Office Supplies`, `Furniture` |
| `Sub-Category` | String | Granular product grouping | 17 sub-categories (e.g., Copiers, Tables, Binders) |
| `Product Name` | String | Descriptive product name | Text |
| `Sales` | Float | Gross transaction revenue ($) | $3.38 to $61,198.74 |
| `Quantity` | Integer | Units ordered in transaction | 1 to 14 units |
| `Discount` | Float | Transaction discount percentage | 0.00 to 0.80 (0% to 80%) |
| `Profit` | Float | Net bottom-line profit ($) | -$6,599.98 to +$24,133.49 |

### Engineered & Derived Features (5 Additional Features in `cleaned_sales.csv`)

| Column Name | Data Type | Formula / Origin | Business Value |
|---|---|---|---|
| `Order Year` | Integer | `Order Date.dt.year` | Annual cohort aggregation (2020, 2021, 2022, 2023) |
| `Order Month` | Integer | `Order Date.dt.month` | Monthly seasonality tracking (1 through 12) |
| `Order Quarter` | Integer | `Order Date.dt.quarter` | Quarterly financial reporting (Q1, Q2, Q3, Q4) |
| `Order DayOfWeek` | Integer | `Order Date.dt.dayofweek` | Day-of-week purchasing patterns (0 = Monday, 6 = Sunday) |
| `Profit Margin %` | Float | `(Profit / Sales) * 100` | Line-item margin efficiency ratio |

---

## 4. File Comparison & Verification

| Property | `raw_sales_data.csv` | `cleaned_sales.csv` | Net Transformation |
|---|---|---|---|
| **Total Rows** | 9,997 | 9,994 | -3 duplicate records removed |
| **Total Columns** | 21 | 26 | +5 derived features engineered |
| **Missing Ship Dates** | 12 (0.12%) | 12 (0.12%) | Retained (legitimate pending orders) |
| **Duplicates** | 3 exact duplicate rows | 0 duplicates | Eliminated |
| **Date Data Types** | String (`object`) | Datetime (`datetime64[ns]`) | Type-cast and validated |
| **Storage Size** | ~2.2 MB | ~2.4 MB | Production CSV format |
