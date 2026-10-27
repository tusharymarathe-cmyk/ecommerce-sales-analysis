# Sales and E-Commerce Performance Analytics Dashboard

**Week 6 Internship Assignment: Git, GitHub & Final Data Analytics Project**  
**Student Name:** Tushar Marathe  
**Internship Organization:** Internova  
**Internship Domain:** Data Analytics  
**Maximum Marks:** 100 | **Duration:** 7 Days  
**Submission Date:** October 2026  
**Repository:** [https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis](https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis)  

---

> **Dataset Disclosure & Methodology:** The dataset analyzed in this project is synthetically generated using calibrated statistical parameters to match the schema and business characteristics of the public Tableau Sample Superstore dataset (`numpy.random.seed(42)`). All business findings, KPIs, visualizations, and strategic recommendations are calculated directly from this dataset for rigorous academic and evaluation purposes.

---

## 1. Project Overview

The **Sales and E-Commerce Performance Analytics Dashboard** is an end-to-end Data Analytics Capstone investigating retail transaction performance, product profitability, customer segment dynamics, regional variations, and the financial impact of discounting strategies.

The project features a fully automated, reproducible Python analytics pipeline, an executed Jupyter Notebook, 10 publication-quality visualizations, an executive 12-page PDF report, a 10-slide executive PowerPoint presentation, production DAX formulas, a Power BI dashboard layout blueprint, and an automated 51-point quality assurance test suite.

---

## 2. Problem Statement

Retail businesses frequently experience rapid top-line sales growth while suffering from unexpected bottom-line margin erosion. Without systematic, granular data analytics, decision-makers are unable to answer:
1. **Profitability Drivers vs. Drags:** Which product categories and specific items generate healthy operating profit versus those that operate at a structural loss?
2. **The Discounting Cliff:** At what exact mathematical threshold does promotional discounting cease to drive incremental revenue and instead destroy net margin?
3. **Regional & Segment Concentration:** How do customer segments (Consumer, Corporate, Home Office) and geographic territories contribute to overall business value?
4. **Demand Trajectory & Seasonality:** When do annual revenue spikes occur, and how should inventory and carrier logistics be pre-allocated?

---

## 3. Project Objectives

1. Ingest, inspect, clean, and feature-engineer raw e-commerce transaction data.
2. Formulate, execute, and validate core business KPIs across categories, regions, and customer segments.
3. Quantify the statistical relationship between discount depth and net profit margins using regression and binning.
4. Generate 10 publication-grade analytical visualizations covering distributions, trends, heatmaps, and rankings.
5. Engineer a complete Power BI dashboard model, production DAX measures library, and 12-column executive layout blueprint.
6. Formulate evidence-based business insights and practical, actionable strategic recommendations.
7. Maintain professional version control hygiene with Git commits, semantic messages, and GitHub synchronization.

---

## 4. Key Performance Indicators (Empirical Results)

*Calculated directly from the cleaned dataset (`data/cleaned_sales.csv`) comprising 9,994 verified transaction line items:*

| Metric | Empirical Value | Business Interpretation |
|---|---|---|
| **Total Gross Sales** | **$33,170,959.70** | Total revenue generated across all 4 operational years (2020–2023) |
| **Total Net Profit** | **$3,642,648.41** | Cumulative operating bottom-line earnings |
| **Overall Profit Margin** | **10.98%** | Operating profit efficiency ratio |
| **Total Units Sold** | **74,555 units** | Total physical product volume shipped |
| **Total Unique Orders** | **9,070 orders** | Cumulative unique customer purchase events |
| **Unique Customers** | **800 accounts** | Total distinct customer base |
| **Average Order Value (AOV)** | **$3,657.22** | Mean gross spend per customer order event |
| **Average Profit per Order** | **$401.62** | Mean bottom-line contribution per order |

---

## 5. Repository Structure

```text
ecommerce-sales-analysis/
│
├── README.md                           # Main comprehensive project documentation
├── requirements.txt                    # Python environment dependencies
├── .gitignore                          # Git exclusions (bytecodes, envs, logs)
├── .gitattributes                     # Normalization for cross-platform line endings
│
├── data/
│   ├── README.md                       # Data dictionary, source & schema documentation
│   ├── raw/
│   │   └── raw_sales_data.csv          # Raw ingested dataset (9,997 rows, 21 columns)
│   ├── processed/
│   │   └── cleaned_sales.csv           # Cleaned & feature-engineered dataset (9,994 rows, 26 columns)
│   ├── raw_sales_data.csv              # Root compatibility link for raw data
│   └── cleaned_sales.csv               # Root compatibility link for cleaned data
│
├── notebooks/
│   ├── final_data_analytics_project.ipynb # Master executed Jupyter Notebook (100% cell outputs)
│   └── EDA_Analysis.ipynb              # Executed EDA notebook copy
│
├── src/
│   ├── analysis.py                     # Master end-to-end pipeline orchestrator
│   ├── data_cleaning.py                # Data cleaning, missing value & outlier handling pipeline
│   ├── eda_analysis.py                 # Statistical EDA & 10 high-res visualization generator
│   ├── build_executed_notebook.py      # Programmatic notebook builder & execution engine
│   ├── create_report.py                # 12-page executive PDF report builder (ReportLab)
│   ├── create_presentation.py          # 10-slide executive PowerPoint builder (python-pptx)
│   └── generate_dataset.py             # Calibrated synthetic data generator (seed=42)
│
├── visualizations/
│   ├── README.md                       # Visualizations catalog, interpretations & metrics
│   ├── 01_sales_by_category.png        # Bar Chart: Sales & Profit by Product Category
│   ├── 02_monthly_sales_trend.png      # Time-Series: 48-Month Sales Trajectory & Seasonality
│   ├── 03_profit_by_region.png         # Horizontal Bar: Regional Net Profit & Margins
│   ├── 04_sales_by_segment.png         # Donut Chart: Customer Segment Revenue Distribution
│   ├── 05_discount_vs_profit.png       # Scatter Plot + OLS: Discount Depth vs. Profitability
│   ├── 06_correlation_heatmap.png      # Triangular Heatmap: Pearson Correlation Matrix
│   ├── 07_top10_products.png           # Horizontal Bar: Top 10 Revenue-Generating SKUs
│   ├── 08_sales_profit_subcategory.png # Comparative Bar: Sub-Category Profitability & Loss Lines
│   ├── 09_yearly_comparison.png        # Multi-Panel Bar: YoY Sales, Profit & Order Volume
│   └── 10_profit_distribution.png      # Box Plots: Profit Dispersion & Legitimate Outliers
│
├── power_bi/
│   ├── README.md                       # Power BI setup instructions & dashboard specification
│   ├── dax_measures.md                 # Complete 18-measure production DAX library
│   └── dashboard_design.md             # 12-column layout grid, coordinates & design system
│
├── reports/
│   ├── final_project_report.pdf        # Publication-ready 12-page executive report (1.01 MB)
│   ├── Final_Data_Analytics_Project_Report.pdf # Formal uppercase report copy
│   ├── business_insights.md            # Empirical business findings & strategic recommendations
│   ├── data_cleaning_summary.md        # Comprehensive data cleaning audit log
│   ├── eda_summary.md                  # Statistical descriptive tables & frequency splits
│   └── assignment_completion_checklist.md # 100-mark audit checklist
│
├── presentation/
│   ├── final_project_presentation.pptx # 10-slide executive presentation deck
│   ├── Final_Project_Presentation.pptx # Alternate casing presentation deck
│   └── Speaker_Notes.md                # Slide-by-slide 5-7 minute executive speech script
│
├── submission/
│   ├── submission_checklist.md         # Requirement-by-requirement verification audit
│   └── final_submission_links.md       # Submission instructions for GitHub, Drive & PDF
│
├── docs/
│   ├── data_dictionary.md              # Detailed column definitions & business ranges
│   ├── git_github_guide.md             # Step-by-step Git commands & workflow guide
│   ├── powerbi_dax_measures.md         # Reference copy of DAX measures
│   └── powerbi_setup_guide.md          # Reference copy of Power BI setup guide
│
└── tests/
    ├── run_tests.py                    # Automated test runner (51/51 checks passed)
    └── test_data_cleaning.py           # Unit tests for data cleaning transformations
```

---

## 6. Data Cleaning & Preparation Pipeline

Implemented in [`src/data_cleaning.py`](src/data_cleaning.py), the cleaning process applies strict, non-destructive transformations:

1. **Initial Inspection:** Loaded 9,997 raw records across 21 columns; identified 6 numerical, 13 categorical, and 2 date features.
2. **Missing Value Resolution:** Identified 12 records (0.12%) with null `Ship Date`. Business logic determined these represent pending, unfulfilled orders. They were intentionally **retained** with explicit documentation rather than dropped.
3. **Duplicate Elimination:** Scanned for exact row duplications; identified and pruned exactly **3 redundant rows**, reducing the dataset to 9,994 records.
4. **Date Parsing & Logic Validation:** Parsed `Order Date` and `Ship Date` into datetime objects; verified that zero records contained chronological violations (`Ship Date < Order Date`).
5. **Range & Logic Verification:** Verified `Sales > 0`, `Quantity > 0`, and confirmed all `Discount` values remained within $[0.0, 1.0]$.
6. **Feature Engineering:** Extracted temporal indicators `Order Year`, `Order Month`, `Order Quarter`, and derived `Profit Margin % = (Profit / Sales) * 100`.
7. **Cleaned Storage:** Exported validated dataset to `data/cleaned_sales.csv` and `data/processed/cleaned_sales.csv`. Full audit log available in [`reports/data_cleaning_summary.md`](reports/data_cleaning_summary.md).

---

## 7. Key Visualizations Overview

All 10 visualizations were programmatically generated at 300 DPI into [`visualizations/`](visualizations/):

| Visual File | Type | Key Analytical Finding |
|---|---|---|
| [`01_sales_by_category.png`](visualizations/01_sales_by_category.png) | Clustered Bar | **Technology** leads in revenue ($11.2M), but **Office Supplies** exhibits the most stable margin consistency. |
| [`02_monthly_sales_trend.png`](visualizations/02_monthly_sales_trend.png) | Time-Series Line | Pronounced **Q4 holiday surge** (November & December account for 34% of annual sales) recurring each year. |
| [`03_profit_by_region.png`](visualizations/03_profit_by_region.png) | Horizontal Bar | All 4 regions are profitable. **West** ($1.12M) and **East** ($1.04M) drive 59.3% of total profit. |
| [`04_sales_by_segment.png`](visualizations/04_sales_by_segment.png) | Donut Chart | **Consumer** generates 52.1% of transactions, while **Corporate** yields an 18% higher Average Order Value. |
| [`05_discount_vs_profit.png`](visualizations/05_discount_vs_profit.png) | Scatter + OLS | Quantifies the **Discounting Cliff**: discounts $>20\%$ cause catastrophic margin collapse. |
| [`06_correlation_heatmap.png`](visualizations/06_correlation_heatmap.png) | Triangular Heatmap | Demonstrates strong negative correlation ($r = -0.854$) between `Discount` and `Profit Margin %`. |
| [`07_top10_products.png`](visualizations/07_top10_products.png) | Horizontal Bar | Enterprise Technology hardware (Copiers, Servers) dominates top gross revenue rankings. |
| [`08_sales_profit_subcategory.png`](visualizations/08_sales_profit_subcategory.png) | Comparative Bar | Isolates **Tables** as a major loss-making sub-category (-$68.4K profit) despite high sales volume. |
| [`09_yearly_comparison.png`](visualizations/09_yearly_comparison.png) | Multi-Panel Bar | Confirms steady year-over-year revenue expansion from FY2020 through FY2023. |
| [`10_profit_distribution.png`](visualizations/10_profit_distribution.png) | Box Plot | Illustrates profit dispersion and verifies that extreme values represent legitimate enterprise bulk orders. |

---

## 8. Power BI Dashboard Architecture

Complete implementation documentation is available in [`power_bi/README.md`](power_bi/README.md), [`power_bi/dax_measures.md`](power_bi/dax_measures.md), and [`power_bi/dashboard_design.md`](power_bi/dashboard_design.md).

### Core DAX Formulas (Exact Dataset Schema Matching)

```dax
-- 1. Total Sales
Total Sales = SUM('cleaned_sales'[Sales])

-- 2. Total Profit
Total Profit = SUM('cleaned_sales'[Profit])

-- 3. Total Orders
Total Orders = DISTINCTCOUNT('cleaned_sales'[Order ID])

-- 4. Profit Margin %
Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0) * 100

-- 5. Average Order Value
Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)

-- 6. Loss Transaction Rate %
Loss Transaction Rate % = 
DIVIDE(
    CALCULATE(COUNTROWS('cleaned_sales'), 'cleaned_sales'[Profit] < 0),
    COUNTROWS('cleaned_sales'),
    0
) * 100
```

### Dashboard Layout & Slicer Hierarchy
- **Canvas Resolution:** 1920 × 1080 (16:9 Widescreen)
- **Top Ribbon:** Canvas Title, Student Credentials, and 4 Global Slicers (`Order Date`, `Region`, `Category`, `Segment`).
- **Upper Zone:** 5 KPI Cards displaying `$33.17M` Sales, `$3.64M` Profit, `10.98%` Margin, `9,070` Orders, and `$3,657.22` AOV.
- **Lower Analytic Tiles:** Monthly Trend Line Chart, Category Clustered Bar, Regional Profit Bar, Segment Donut, and Top 10 Products Ranking.

> **Power BI Desktop Notice:** Power BI Desktop is installed locally (`Microsoft.MicrosoftPowerBIDesktop_8wekyb3d8bbwe`). Because Power BI does not support headless CLI generation of binary `.pbix` files, the dataset, DAX measures, and design blueprints are prepared so the `.pbix` file can be opened and saved directly in Power BI Desktop without generating invalid placeholders.

---

## 9. Key Business Insights

1. **The 20% Discount Cliff (Margin Destruction):**
   - Transactions with 0% discount average **+$577.80** profit per order (0% loss rate).
   - Transactions with 11–20% discount remain profitable (**+$311.20** average profit).
   - Discounts exceeding 20% produce widespread losses: 21–30% discount yields an average loss of **-$142.50** (38.4% loss rate), and 50%+ discounts produce **-$780.10** average loss (86.2% loss rate).
   - Correlation between Discount and Profit Margin % is **r = -0.854**.

2. **Sub-Category Profitability Discrepancy:**
   - **Tables** generates $1.7M in revenue but operates at a cumulative **-$68,420 net loss** due to excessive promotional discounting and high carrier freight costs.
   - Conversely, **Copiers** and **Phones** generate high sales with healthy profit margins exceeding 14%.

3. **Predictable Q4 Seasonal Demand Surge:**
   - November and December reliably account for **34% of annual gross sales** across all four operating years, driven by enterprise year-end budget flushes and holiday consumer demand.

4. **Regional Profit Dominance:**
   - The **West** ($1.12M profit) and **East** ($1.04M profit) regions drive 59.3% of total company profit.
   - The **South** achieves the highest individual profit margin efficiency at **12.4%**.

5. **Customer Segment Value Dynamics:**
   - While **Consumer** accounts represent 52.1% of transactions, **Corporate** accounts generate an 18% higher Average Order Value ($3,840 vs. $3,520), reflecting higher bulk purchase propensity.

---

## 10. Strategic Business Recommendations

1. **Implement Automated Discount Governance Policy:**
   - Configure a hard price ceiling restricting sales representative discretionary discounts to **15%**.
   - Require formal VP approval for discounts between 15% and 20%. Prohibit discounts above 20% except for non-performing inventory liquidation.
   - *Expected Benefit:* Eliminates unnecessary margin destruction and raises aggregate net profit margin from 10.98% to ~12.5%.

2. **Restructure Loss-Making Product Lines (Tables Sub-Category):**
   - Renegotiate manufacturer acquisition costs and unbundle freight shipping fees for oversized furniture items.
   - Transition chronically negative SKUs to direct vendor drop-shipping.
   - *Expected Benefit:* Stems the $68K annual drain from Tables and restores category-level operating profitability.

3. **Proactive Q3 Supply Chain & Carrier Buffering:**
   - Pre-book warehouse labor and carrier freight commitments in August/September ahead of the proven Q4 volume surge.
   - *Expected Benefit:* Protects service delivery standards and avoids expedited peak-season carrier surcharges.

4. **Corporate Account Tiering & Volume Rebates:**
   - Replace upfront invoice discounts with backend annual volume rebates for Corporate and Home Office clients.
   - *Expected Benefit:* Secures higher annual contract volume while preserving baseline transaction margin integrity.

---

## 11. Git & GitHub Workflow Practice

This repository serves as a hands-on demonstration of professional Git version control standards:

### Core Git Commands Demonstrated

```bash
# 1. Clone Repository
git clone https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis

# 2. Check Repository Status
git status

# 3. Stage Modified or New Files
git add .

# 4. Create Meaningful Commit
git commit -m "Implement end-to-end data analytics pipeline and executed notebook"

# 5. Push Commits to Remote GitHub Repository
git push origin main

# 6. Pull Remote Changes
git pull origin main
```

### Commit History Highlights
- `39d8349`: Initial project structure, configurations, and environment setup
- `bccfdf3`: Add synthetic dataset, data cleaning pipeline, and data dictionary
- `e9146bd`: Add EDA script, statistical summary, and 10 visualizations
- `7cca80a`: Add Power BI documentation, DAX measures, and Jupyter Notebook
- `d212641`: Add business insights, executive presentation, and formal PDF report
- `12e0b84`: Add automated test suite and test runner
- `7402ad4`: Add automated generators for notebook, presentation, and PDF report
- `2bcf8a7`: Update README with author profile and official repository URL
- Subsequent commits: Finalize executed notebook, master pipeline runner, submission checklists, and presentation assets.

---

## 12. Verification & Testing

The repository contains an automated test suite executed via [`tests/run_tests.py`](tests/run_tests.py) or [`src/analysis.py`](src/analysis.py):

```bash
python tests/run_tests.py
```

### Test Suite Results: 51/51 Checks Passed (100%)
- **Group 1: File Existence (5/5)** — Raw CSV, Cleaned CSV, Cleaning Report, EDA Report, Business Insights.
- **Group 2: Dataset Dimensions (3/3)** — Verified $\ge 9,000$ rows, confirmed non-destructive duplicate reduction.
- **Group 3: Schema Conformance (12/12)** — Validated presence and data types of all 12 core business features.
- **Group 4: Derived Features (4/4)** — Validated `Order Year`, `Order Month`, `Order Quarter`, `Profit Margin %`.
- **Group 5: Data Quality (5/5)** — 0 duplicate rows, Sales $>0$, Quantity $>0$, Discount $\in [0, 1]$, valid Datetime.
- **Group 6: Business Rules (11/11)** — 3 categories, 4 regions, 3 segments, years 2020–2023, months 1–12, quarters 1–4, $\ge 100$ customers, $\ge 50$ products.
- **Group 7: Visualizations (11/11)** — Verified all 10 PNG charts generated, non-empty, and correctly formatted.

---

## 13. Instructions to Run the Project

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Git 2.30+

### Quick Start (One Command)

```bash
# 1. Clone repository
git clone https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute master end-to-end pipeline
python src/analysis.py
```

Running `python src/analysis.py` automatically performs:
1. Data cleaning and feature engineering (`src/data_cleaning.py`)
2. Statistical EDA and 10 high-resolution charts (`src/eda_analysis.py`)
3. Jupyter Notebook build and full cell execution (`src/build_executed_notebook.py`)
4. Executive 12-page PDF report generation (`src/create_report.py`)
5. Executive PowerPoint presentation generation (`src/create_presentation.py`)
6. Quality assurance test runner (`tests/run_tests.py`)

---

## 14. Submission Package Links

- **GitHub Repository:** [https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis](https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis)
- **Executive PDF Report:** [`reports/final_project_report.pdf`](reports/final_project_report.pdf) (1.01 MB)
- **Executed Jupyter Notebook:** [`notebooks/final_data_analytics_project.ipynb`](notebooks/final_data_analytics_project.ipynb)
- **PowerPoint Presentation:** [`presentation/final_project_presentation.pptx`](presentation/final_project_presentation.pptx)
- **Submission Checklist:** [`submission/submission_checklist.md`](submission/submission_checklist.md)
- **Submission Links Guide:** [`submission/final_submission_links.md`](submission/final_submission_links.md)

---

## 15. Author & Credentials

- **Student Name:** Tushar Marathe
- **Organization:** Internova
- **Domain:** Data Analytics
- **Assignment:** Week 6 — Git, GitHub & Final Data Analytics Project
- **GitHub Profile:** [@tusharymarathe-cmyk](https://github.com/tusharymarathe-cmyk)
- **Repository:** [https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis](https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis)
- **License:** MIT License
