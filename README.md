# E-Commerce Sales Data Analysis and Interactive Power BI Dashboard

**Week 6 Internship Assignment: Git, GitHub & Final Data Analytics Project**  
**Student Name:** [Your Name]  
**Submission Date:** October 2026  
**Total Marks:** 100 | **Duration:** 7 Days

---

> ⚠️ **Dataset Notice**: The dataset used in this project is synthetically generated using calibrated statistical parameters to match the schema and characteristics of the public Tableau Sample Superstore dataset. All findings, KPI values, and business recommendations are calculated directly from this synthetic data for educational and evaluation purposes.

---

## 1. Project Overview

This project is an end-to-end Data Analytics Capstone designed to analyze retail e-commerce sales performance, product profitability, customer segment distributions, regional variations, and the direct financial impact of discounting strategies. The project culminates in an automated exploratory data analysis pipeline, 10 high-resolution visualizations, a comprehensive 12-page professional PDF report, an executive PowerPoint presentation, and an interactive Power BI dashboard architecture.

---

## 2. Problem Statement

Retail businesses often experience high top-line revenue growth while facing shrinking net profit margins. Without systematic, granular analysis, decision-makers cannot determine:
1. Which specific products or categories drive bottom-line profits versus those that operate at a loss.
2. The quantitative tipping point where discounting transitions from a revenue driver to a margin destroyer.
3. How regional performance and customer segments contribute to overall business health.
4. How seasonal demand spikes (e.g., Q4 holiday surge) should inform supply chain and inventory planning.

---

## 3. Project Objectives

1. Ingest, clean, validate, and feature-engineer raw e-commerce transaction data.
2. Evaluate sales and net profit across product categories, sub-categories, regions, and customer segments.
3. Quantify the statistical relationship between discount depth and profit margins.
4. Generate 10 publication-quality visualizations covering distributions, trends, and correlations.
5. Formulate Power BI dashboard layout, data models, and DAX measures.
6. Derive evidence-based business insights and actionable strategic recommendations.
7. Prepare a publication-ready GitHub repository with strict version control hygiene.

---

## 4. Key Performance Indicators (Actual Results)

*Calculated directly from the cleaned dataset (`data/cleaned_sales.csv`) comprising 9,994 records:*

| Metric | Value |
|---|---|
| **Total Gross Sales** | **$33,170,959.70** |
| **Total Net Profit** | **$3,642,648.41** |
| **Overall Profit Margin** | **10.98%** |
| **Total Units Sold** | **74,555 units** |
| **Total Unique Orders** | **9,070 orders** |
| **Unique Customers** | **800 customers** |
| **Average Order Value (AOV)** | **$3,657.22** |

---

## 5. Repository Structure

```text
ecommerce-sales-analysis/
├── .gitattributes                     # Git line-ending normalization
├── .gitignore                          # Standard Python, data, & OS exclusions
├── README.md                           # Main project documentation (this file)
├── requirements.txt                    # Python dependencies
├── data/
│   ├── README.md                       # Dataset overview and license details
│   ├── raw_sales_data.csv              # Raw synthetic dataset (9,997 rows)
│   └── cleaned_sales.csv               # Processed dataset (9,994 rows, 26 cols)
├── notebooks/
│   └── EDA_Analysis.ipynb              # Executable Jupyter notebook with analysis
├── src/
│   ├── generate_dataset.py             # Reproducible synthetic dataset generator
│   ├── data_cleaning.py                # Data cleaning and validation pipeline
│   ├── eda_analysis.py                 # EDA calculations and chart generation
│   ├── create_notebook.py              # Programmatic notebook builder
│   ├── create_presentation.py          # PowerPoint deck generator (python-pptx)
│   └── create_report.py                # Academic/business PDF report generator
├── visualizations/
│   ├── README.md                       # Detailed chart catalog and decision value
│   ├── 01_sales_by_category.png        # Bar chart: Sales by category
│   ├── 02_monthly_sales_trend.png      # Line chart: Monthly sales trend (2020-2023)
│   ├── 03_profit_by_region.png         # Bar chart: Profit by region
│   ├── 04_sales_by_segment.png         # Donut & bar combo: Customer segments
│   ├── 05_discount_vs_profit.png       # Scatter plot: Discount rate vs. profit
│   ├── 06_correlation_heatmap.png      # Heatmap: Numerical variables
│   ├── 07_top10_products.png           # Horizontal bar: Top 10 selling products
│   ├── 08_sales_profit_subcategory.png # Comparative bar: Sales vs profit
│   ├── 09_yearly_comparison.png        # Bar charts: YoY comparison
│   └── 10_profit_distribution.png      # Box plot: Profit distribution by category
├── powerbi/
│   ├── README.md                       # Dashboard architecture and layout spec
│   └── Ecommerce_Sales_Dashboard.pbix  # Target location for Power BI dashboard file
├── reports/
│   ├── data_cleaning_summary.md        # Audit log of data transformations
│   ├── eda_summary.md                  # Statistical summary & frequency tables
│   ├── business_insights.md            # In-depth business insights & recommendations
│   ├── assignment_completion_checklist.md # 100-mark audit rubric
│   └── Final_Data_Analytics_Project_Report.pdf # 12+ page formal PDF report
├── presentation/
│   ├── Final_Project_Presentation.pptx # 10-slide executive slide deck
│   └── Speaker_Notes.md                # 5-7 min spoken presentation script
├── docs/
│   ├── data_dictionary.md              # Complete column definitions & metadata
│   ├── powerbi_setup_guide.md          # Step-by-step Power BI import & build steps
│   ├── powerbi_dax_measures.md         # Production-ready DAX measure formulas
│   └── git_github_guide.md             # Git concepts, commands, and workflow guide
└── tests/
    ├── test_data_cleaning.py           # Pytest test suite
    └── run_tests.py                    # Standalone test runner (51 validation checks)
```

---

## 6. Data Cleaning & Preparation Pipeline

Implemented in [`src/data_cleaning.py`](src/data_cleaning.py):
1. **Deduplication**: Identified and removed 3 exact duplicate rows.
2. **Missing Value Treatment**: 12 records exhibited null `Ship Date` entries; these were identified as legitimate unshipped/in-transit orders and retained without artificial imputation.
3. **Data Type Casting**: Normalized all order and shipping dates to `datetime64[ns]`.
4. **Range & Logic Validation**: Checked that `Sales > 0`, `Quantity > 0`, and verified `Discount` values remained within $[0.0, 1.0]$.
5. **Feature Engineering**: Extracted temporal features (`Order Year`, `Order Month`, `Order Month Name`, `Order Quarter`) and calculated row-level `Profit Margin %`.
6. **Outlier Assessment**: Evaluated 1,733 records with extreme values ($> 3 \times \text{IQR}$). These records reflect legitimate commercial bulk purchases and were intentionally preserved to prevent negative bias in volume calculations.

Full transformation log is available in [`reports/data_cleaning_summary.md`](reports/data_cleaning_summary.md).

---

## 7. Key Visualizations Overview

| Chart | Filename | Key Business Takeaway |
|---|---|---|
| **Sales by Category** | [`01_sales_by_category.png`](visualizations/01_sales_by_category.png) | Technology generates the highest sales volume, followed closely by Office Supplies. |
| **Monthly Sales Trend** | [`02_monthly_sales_trend.png`](visualizations/02_monthly_sales_trend.png) | Pronounced Q4 holiday demand spike occurring reliably across all 4 recorded years. |
| **Profit by Region** | [`03_profit_by_region.png`](visualizations/03_profit_by_region.png) | All 4 geographic regions are profitable; West and East account for dominant volume. |
| **Sales by Segment** | [`04_sales_by_segment.png`](visualizations/04_sales_by_segment.png) | Consumers comprise 52.1% of transactions; Corporate accounts generate higher order values. |
| **Discount vs. Profit** | [`05_discount_vs_profit.png`](visualizations/05_discount_vs_profit.png) | Linear regression line proves discounts exceeding 20% result in widespread negative profit. |
| **Correlation Heatmap** | [`06_correlation_heatmap.png`](visualizations/06_correlation_heatmap.png) | Strong negative correlation ($r = -0.854$) between Discount and Profit Margin %. |
| **Top 10 Products** | [`07_top10_products.png`](visualizations/07_top10_products.png) | High-ticket technology products (Copiers, Machines) dominate top sales rankings. |
| **Sales vs Profit by Sub-Cat** | [`08_sales_profit_subcategory.png`](visualizations/08_sales_profit_subcategory.png) | Identifies Tables as a loss-generating sub-category despite significant sales volume. |
| **Year-over-Year Summary** | [`09_yearly_comparison.png`](visualizations/09_yearly_comparison.png) | Demonstrates consistent annual transaction growth and steady revenue expansion. |
| **Profit Distribution** | [`10_profit_distribution.png`](visualizations/10_profit_distribution.png) | Visualizes extreme profit variance and outlier clusters in Furniture and Technology. |

---

## 8. Power BI Dashboard Architecture

*Detailed documentation: [`docs/powerbi_setup_guide.md`](docs/powerbi_setup_guide.md) & [`docs/powerbi_dax_measures.md`](docs/powerbi_dax_measures.md)*

### Core DAX Measures
```dax
Total Sales = SUM('cleaned_sales'[Sales])

Total Profit = SUM('cleaned_sales'[Profit])

Total Orders = DISTINCTCOUNT('cleaned_sales'[Order ID])

Profit Margin % = DIVIDE([Total Profit], [Total Sales], 0) * 100

Average Order Value = DIVIDE([Total Sales], [Total Orders], 0)
```

### Layout Specification
- **Top Ribbon**: 4 KPI Cards (`Total Sales`, `Total Profit`, `Total Orders`, `Profit Margin %`).
- **Filter Pane / Slicers**: Order Date Range, Region dropdown, Category tiles, Customer Segment tiles.
- **Center Visual**: Full-width Line Chart displaying Monthly Sales Trends across years.
- **Mid-Tier Visuals**: Clustered Bar (Sales by Category), Clustered Bar (Profit by Region), Donut (Segment Share).
- **Bottom Visual**: Top 10 Products by Sales Bar Chart.

---

## 9. Key Business Insights

1. **Discounting Destroys Margins**: Pearson correlation between `Discount` and `Profit Margin %` is **-0.854**. Discounts above 20% routinely tip transactions into negative net profits.
2. **Technology Category Advantage**: Technology leads total sales volume; sub-categories like Copiers provide high baseline unit profit margins (~38%).
3. **Structural Loss in Furniture Tables**: The Tables sub-category yields negative overall profit margins (-5.0%), indicating pricing that fails to cover cost of goods and fulfillment.
4. **Reliable Q4 Seasonality**: October through December consistently outperform January and February by 20% to 35% in gross revenue.
5. **Corporate Account Potential**: While Consumer accounts generate 52.1% of transactions, Corporate buyers purchase larger quantities with lower price sensitivity.

---

## 10. Strategic Business Recommendations

1. **Enforce a Discount Governance Policy**:
   - Establish a hard ceiling of 20% maximum discount across standard sales operations.
   - Mandate senior finance approval for discounts exceeding 20%.
   - Replace heavy flat percentage discounts with multi-item bundle incentives (e.g., Buy 3, Get 1 Free).
2. **Execute a Dedicated Corporate Segment Strategy**:
   - Assign dedicated account representatives to the top 100 lifetime-value Corporate clients.
   - Introduce pre-negotiated tiered volume pricing to capture higher bulk order margins.
3. **Reprice the Furniture Tables Portfolio**:
   - Review and adjust baseline MSRP on Tables to secure a minimum 5% gross profit margin.
   - Restrict all discounting on Tables until profitability stabilizes.

---

## 11. Verification and Testing

The repository contains an automated test suite executed via [`tests/run_tests.py`](tests/run_tests.py).
- **Total Tests**: 51
- **Passed**: 51
- **Failed**: 0
- **Pass Rate**: 100%

Coverage includes file integrity, schema consistency, data range validity, derived column validation, categorical boundary checks, and visualization asset generation.

---

## 12. Instructions to Run the Project

### Prerequisites
- Python 3.10+ installed
- Git installed

### Setup & Execution
```bash
# 1. Clone repository
git clone https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Regenerate dataset and clean data
python src/generate_dataset.py
python src/data_cleaning.py

# 4. Run exploratory data analysis and generate charts
python src/eda_analysis.py

# 5. Run automated test suite
python tests/run_tests.py

# 6. Generate presentation and PDF report
python src/create_presentation.py
python src/create_report.py
```

---

## 13. Author & License

- **Author**: Tushar Marathe ([@tusharymarathe-cmyk](https://github.com/tusharymarathe-cmyk))
- **Repository**: [https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis](https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis)
- **Assignment**: Week 6 Final Data Analytics Project
- **License**: MIT License - Free for educational and analytical use.
