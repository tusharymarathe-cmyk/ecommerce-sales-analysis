# Assignment Completion Checklist & Requirement Audit

**Project**: E-Commerce Sales Data Analysis and Interactive Power BI Dashboard  
**Assignment**: Week 6 Assignment: Git, GitHub & Final Data Analytics Project  
**Total Marks**: 100  
**Audit Date**: October 25, 2026  

---

## Task-by-Task Evaluation Matrix

| Task # | Task Description | Total Marks | Status | Evidence / Artifacts |
|---|---|---|---|---|
| **Task 1** | **Git & GitHub Basics** | 10 | **COMPLETED AND VERIFIED** | `docs/git_github_guide.md`, repository `.gitignore`, `.gitattributes` |
| **Task 2** | **Git Workflow Practice** | 10 | **COMPLETED AND VERIFIED** | Granular local Git commits, verified commit log, clean git staging |
| **Task 3** | **Dataset Selection & Preparation** | 10 | **COMPLETED AND VERIFIED** | `data/raw_sales_data.csv`, `data/cleaned_sales.csv`, `src/data_cleaning.py`, `reports/data_cleaning_summary.md`, `docs/data_dictionary.md` |
| **Task 4** | **Exploratory Data Analysis** | 15 | **COMPLETED AND VERIFIED** | `notebooks/EDA_Analysis.ipynb`, `src/eda_analysis.py`, `reports/eda_summary.md` |
| **Task 5** | **Data Visualization** | 15 | **COMPLETED AND VERIFIED** | 10 high-resolution charts in `visualizations/`, `visualizations/README.md` |
| **Task 6** | **Power BI Dashboard** | 20 | **COMPLETED BUT NOT FULLY VERIFIED** | `powerbi/README.md`, `docs/powerbi_setup_guide.md`, `docs/powerbi_dax_measures.md` *(manual `.pbix` creation required in desktop app)* |
| **Task 7** | **Business Insights & Recommendations** | 10 | **COMPLETED AND VERIFIED** | 6 evidence-based insights, 3 strategic recommendations in `reports/business_insights.md` |
| **Task 8** | **GitHub Documentation & Presentation** | 10 | **COMPLETED AND VERIFIED** | Root `README.md`, `presentation/Final_Project_Presentation.pptx`, `presentation/Speaker_Notes.md`, `reports/Final_Data_Analytics_Project_Report.pdf` |

---

## Detailed Audit Breakdown

### Task 1: Git & GitHub Basics (10 Marks)
- **Status**: COMPLETED AND VERIFIED
- **Audit Findings**:
  - Comprehensive guide written in [`docs/git_github_guide.md`](../docs/git_github_guide.md) covering clone, status, add, commit, push, pull, log, and remote repository creation.
  - Production-ready [`.gitignore`](../.gitignore) excludes environments, `.ipynb_checkpoints`, bytecodes, and OS metadata.
  - Line ending normalization configured in [`.gitattributes`](../.gitattributes).

### Task 2: Git Workflow Practice (10 Marks)
- **Status**: COMPLETED AND VERIFIED
- **Audit Findings**:
  - Logical progression of modular commits covering initial architecture, cleaning scripts, EDA visualizations, reports, and documentation.
  - No credentials, tokens, or personal identifiers committed.

### Task 3: Dataset Selection & Preparation (10 Marks)
- **Status**: COMPLETED AND VERIFIED
- **Audit Findings**:
  - Raw dataset generated via [`src/generate_dataset.py`](../src/generate_dataset.py) matching Superstore schema (9,997 rows, 21 columns).
  - Explicit documentation specifying synthetic nature for academic honesty.
  - Complete data dictionary created in [`docs/data_dictionary.md`](../docs/data_dictionary.md).
  - Cleaning pipeline executed via [`src/data_cleaning.py`](../src/data_cleaning.py), producing `data/cleaned_sales.csv` (9,994 rows, 26 columns).
  - Data cleaning audit log compiled in [`reports/data_cleaning_summary.md`](../reports/data_cleaning_summary.md).

### Task 4: Exploratory Data Analysis (15 Marks)
- **Status**: COMPLETED AND VERIFIED
- **Audit Findings**:
  - Complete, structured Jupyter notebook at [`notebooks/EDA_Analysis.ipynb`](../notebooks/EDA_Analysis.ipynb) containing Markdown narrative, inspection cells, descriptive stats, outlier decisions, and business questions.
  - Standalone script at [`src/eda_analysis.py`](../src/eda_analysis.py) calculating all KPI figures and category/regional aggregations.
  - Detailed statistical summary table in [`reports/eda_summary.md`](../reports/eda_summary.md).

### Task 5: Data Visualization (15 Marks)
- **Status**: COMPLETED AND VERIFIED
- **Audit Findings**:
  - 10 charts created and saved as 150 DPI PNGs in [`visualizations/`](../visualizations/):
    1. `01_sales_by_category.png` (Sales by category bar chart)
    2. `02_monthly_sales_trend.png` (Monthly sales trend line chart)
    3. `03_profit_by_region.png` (Profit by region horizontal bar)
    4. `04_sales_by_segment.png` (Customer segment donut & bar combo)
    5. `05_discount_vs_profit.png` (Scatter plot with trendline)
    6. `06_correlation_heatmap.png` (Annotated numerical correlation matrix)
    7. `07_top10_products.png` (Horizontal bar for top products)
    8. `08_sales_profit_subcategory.png` (Comparative sales & profit chart)
    9. `09_yearly_comparison.png` (Multi-panel year-over-year bar chart)
    10. `10_profit_distribution.png` (Profit distribution box plot)
  - Detailed documentation catalog in [`visualizations/README.md`](../visualizations/README.md).

### Task 6: Power BI Dashboard (20 Marks)
- **Status**: COMPLETED BUT NOT FULLY VERIFIED (Requires Manual Action)
- **Audit Findings**:
  - Automated desktop GUI generation of `.pbix` files is impossible without human interaction in Power BI Desktop.
  - Complete build specification delivered in [`docs/powerbi_setup_guide.md`](../docs/powerbi_setup_guide.md).
  - Production-ready DAX measures delivered in [`docs/powerbi_dax_measures.md`](../docs/powerbi_dax_measures.md).
  - Layout wireframe and card specs documented in [`powerbi/README.md`](../powerbi/README.md).
  - Cleaned data source verified and available at `data/cleaned_sales.csv`.

### Task 7: Business Insights & Recommendations (10 Marks)
- **Status**: COMPLETED AND VERIFIED
- **Audit Findings**:
  - 6 quantitative insights with exact metrics documented in [`reports/business_insights.md`](../reports/business_insights.md).
  - Key finding identified: Discount vs Profit Margin correlation of **-0.854** (discounts >20% create losses).
  - Structural loss in Tables sub-category identified.
  - 3 actionable, structured recommendations with implementation complexity and impact estimates provided.

### Task 8: GitHub Documentation & Presentation (10 Marks)
- **Status**: COMPLETED AND VERIFIED
- **Audit Findings**:
  - Root [`README.md`](../README.md) formatted with Markdown tables, project architecture, KPI results, execution guide, and file links.
  - Professional 10-slide PowerPoint presentation generated in [`presentation/Final_Project_Presentation.pptx`](../presentation/Final_Project_Presentation.pptx).
  - Full spoken script in [`presentation/Speaker_Notes.md`](../presentation/Speaker_Notes.md).
  - 17-section formal PDF report compiled in [`reports/Final_Data_Analytics_Project_Report.pdf`](../reports/Final_Data_Analytics_Project_Report.pdf) (1.01 MB).

---

## Automated Verification Test Results
Executed via `tests/run_tests.py`:
- **File Integrity Checks**: Passed (5/5)
- **Dataset Size Checks**: Passed (3/3)
- **Required Columns**: Passed (12/12)
- **Derived Columns**: Passed (4/4)
- **Data Quality Logic**: Passed (5/5)
- **Business Domain Rules**: Passed (11/11)
- **Visualization Artifacts**: Passed (11/11)
- **Total Test Score**: **51 / 51 Passed (100%)**
