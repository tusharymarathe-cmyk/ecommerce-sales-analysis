# Power BI Dashboard
## E-Commerce Sales & Profitability Analytics Dashboard

---

## Dashboard Status

> **⚠️ Manual Action Required:** Power BI Desktop is a Windows GUI application that cannot be automated through the command line in this environment. The `.pbix` file must be created manually using Power BI Desktop.

The complete preparation materials for building the dashboard are provided:

| File | Purpose |
|------|---------|
| `../data/cleaned_sales.csv` | Data source for Power BI |
| `../docs/powerbi_setup_guide.md` | Step-by-step setup instructions |
| `../docs/powerbi_dax_measures.md` | All required DAX formulas |

---

## Dashboard Specifications

**Title:** E-Commerce Sales & Profitability Analytics Dashboard  
**Data Source:** `data/cleaned_sales.csv` (9,994 rows, 26 columns)  
**Date Range:** January 2020 – December 2023

---

## Required KPI Cards

| Card | Measure | Format |
|------|---------|--------|
| Total Sales | SUM(Sales) | Currency (\$) |
| Total Profit | SUM(Profit) | Currency (\$) |
| Total Orders | DISTINCTCOUNT(Order ID) | Whole number |
| Profit Margin % | Profit / Sales × 100 | Percentage |

---

## Required Visualizations

| # | Visual Type | X/Category | Y/Value | Notes |
|---|------------|------------|---------|-------|
| 1 | Line Chart | Order Date (Month) | Total Sales | Trend across 4 years |
| 2 | Bar Chart | Category | Total Sales | 3 categories |
| 3 | Bar Chart | Region | Total Profit | Color-coded by value |
| 4 | Donut Chart | Segment | Total Sales | 3 segments |
| 5 | Horizontal Bar | Product Name | Total Sales | Top 10 filter |

---

## Required Slicers

| Slicer | Field | Style |
|--------|-------|-------|
| Date Range | Order Date | Date picker |
| Region | Region | Dropdown |
| Category | Category | List |
| Customer Segment | Segment | List |

---

## Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  📊 E-Commerce Sales & Profitability Analytics Dashboard                    │
│                                                                             │
│  [Order Date ▼]  [Region ▼]  [Category ▼]  [Segment ▼]                     │
├─────────────┬─────────────┬─────────────┬─────────────────────────────────  │
│ Total Sales │Total Profit │Total Orders │    Profit Margin %                │
│ $33.17M     │  $3.64M     │   9,070     │       10.98%                      │
├─────────────┴─────────────┴─────────────┴─────────────────────────────────  │
│                                                                             │
│           Monthly Sales Trend (2020–2023)                                   │
│           ─────────────────────────────────────────────                     │
│                                                                             │
├──────────────────┬──────────────────┬──────────────────────────────────────│
│  Sales by        │  Profit by       │  Sales by Customer                   │
│  Category        │  Region          │  Segment                             │
│  [Bar Chart]     │  [Bar Chart]     │  [Donut Chart]                       │
├──────────────────┴──────────────────┴──────────────────────────────────────│
│                                                                             │
│           Top 10 Products by Sales                                          │
│           ─────────────────────────────────────────────                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## How to Build the Dashboard

1. Complete: See `docs/powerbi_setup_guide.md` for detailed instructions
2. Data: Use `data/cleaned_sales.csv`
3. DAX: Copy measures from `docs/powerbi_dax_measures.md`
4. Save as: `powerbi/Ecommerce_Sales_Dashboard.pbix`

---

## Expected .pbix File Location

Once built manually:
```
powerbi/
└── Ecommerce_Sales_Dashboard.pbix  ← Save here after building in Power BI Desktop
```

---

*Power BI dashboard preparation — Week 6 Internship Assignment*
