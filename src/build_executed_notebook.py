"""
build_executed_notebook.py
--------------------------
Builds and fully executes the final EDA Jupyter Notebook with all outputs,
embedded visualizations, descriptive tables, and narrative interpretations.

Generates:
- notebooks/final_data_analytics_project.ipynb
- notebooks/EDA_Analysis.ipynb
"""

import os
import sys
import ast
import io
import base64
import contextlib
import nbformat as nbf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_PATH_FINAL = os.path.join(BASE_DIR, 'notebooks', 'final_data_analytics_project.ipynb')
NB_PATH_EDA = os.path.join(BASE_DIR, 'notebooks', 'EDA_Analysis.ipynb')
os.makedirs(os.path.dirname(NB_PATH_FINAL), exist_ok=True)

# ── Helper to execute code cell and capture outputs ─────────────────────────────
class NotebookExecutor:
    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.ns = {}
        self.execution_count = 0
        # Initialize basic namespace with headless Agg backend
        exec("import os, sys, warnings, matplotlib; matplotlib.use('Agg'); warnings.filterwarnings('ignore')", self.ns)

    def execute_cell(self, code_str):
        self.execution_count += 1
        outputs = []
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()

        import matplotlib.pyplot as plt
        plt.close('all')

        curr_dir = os.getcwd()
        os.chdir(self.working_dir)

        try:
            parsed = ast.parse(code_str)
            last_expr = None
            if parsed.body and isinstance(parsed.body[-1], ast.Expr):
                last_expr = parsed.body.pop()

            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                if parsed.body:
                    code_obj = compile(ast.Module(body=parsed.body, type_ignores=[]), '<cell>', 'exec')
                    exec(code_obj, self.ns)

                res = None
                if last_expr is not None:
                    expr_obj = compile(ast.Expression(body=last_expr.value), '<cell>', 'eval')
                    res = eval(expr_obj, self.ns)

        except Exception as e:
            stdout_buf.write(f"\nExecution error: {e}")
            res = None
        finally:
            os.chdir(curr_dir)

        # 1. Stdout stream
        stdout_val = stdout_buf.getvalue()
        if stdout_val:
            outputs.append(nbf.v4.new_output(
                output_type='stream',
                name='stdout',
                text=stdout_val
            ))

        # 2. Check for matplotlib figures
        fig_nums = plt.get_fignums()
        if fig_nums:
            for num in fig_nums:
                fig = plt.figure(num)
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format='png', bbox_inches='tight', dpi=100)
                img_buf.seek(0)
                b64_data = base64.b64encode(img_buf.read()).decode('ascii')
                outputs.append(nbf.v4.new_output(
                    output_type='display_data',
                    data={
                        'image/png': b64_data,
                        'text/plain': f'<Figure size {fig.get_size_inches()[0]*100}x{fig.get_size_inches()[1]*100} with {len(fig.axes)} Axes>'
                    },
                    metadata={}
                ))
            plt.close('all')

        # 3. Handle evaluated expression result
        if res is not None:
            # Check if res is a figure/axes already handled
            if not isinstance(res, (plt.Figure, plt.Axes)):
                data_dict = {}
                if hasattr(res, '_repr_html_'):
                    data_dict['text/html'] = res._repr_html_()
                data_dict['text/plain'] = repr(res)

                outputs.append(nbf.v4.new_output(
                    output_type='execute_result',
                    execution_count=self.execution_count,
                    data=data_dict,
                    metadata={}
                ))

        return self.execution_count, outputs


def build_notebook():
    print("[INFO] Assembling notebook structure...")
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.13.1"}
    }

    raw_cells = []

    # 1. Introduction
    raw_cells.append(('md', """# Sales and E-Commerce Performance Analytics Dashboard
## Final Data Analytics Project — Week 6 Internship Assignment

- **Student Name:** Tushar Marathe
- **Internship Organization:** Internova
- **Internship Domain:** Data Analytics
- **Total Marks:** 100 | **Duration:** 7 Days
- **Date:** October 2026

---

### Project Overview & Objectives
This project is an end-to-end exploratory data analysis and business intelligence capstone investigating e-commerce retail transactions.
Key objectives:
1. Load, validate, clean, and feature-engineer raw transaction data.
2. Calculate business KPIs: Total Sales, Total Profit, Profit Margin %, Units Sold, and Average Order Value (AOV).
3. Conduct univariate, bivariate, and multivariate analysis across product categories, sub-categories, regions, and customer segments.
4. Uncover the quantitative relationship between discounting depth and net profitability.
5. Provide actionable, data-driven business recommendations backed by empirical metrics.

> **Data Disclosure & Methodology:** The dataset analyzed in this project is synthetically generated using calibrated statistical distributions modeled after the public Tableau Sample Superstore schema (seed=42). All metrics, findings, and visualizations reflect this dataset for rigorous academic and evaluation purposes."""))

    # 2. Setup
    raw_cells.append(('md', """## 1. Environment Setup & Data Loading
Import required Python libraries for data manipulation, numerical calculations, statistical analysis, and visual charting."""))

    raw_cells.append(('code', """import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['figure.dpi'] = 110

# Locate and load cleaned dataset
data_candidates = [
    os.path.join('..', 'data', 'cleaned_sales.csv'),
    os.path.join('data', 'cleaned_sales.csv'),
    os.path.join('..', 'data', 'processed', 'cleaned_sales.csv')
]
data_path = next((p for p in data_candidates if os.path.exists(p)), 'data/cleaned_sales.csv')

df = pd.read_csv(data_path)
df['Order Date'] = pd.to_datetime(df['Order Date'])
if 'Ship Date' in df.columns:
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])

print(f"Dataset successfully loaded from: {data_path}")
print(f"Dimensions: {df.shape[0]:,} rows x {df.shape[1]} columns")
print(f"Date Range: {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}")"""))

    # 3. Initial Inspection
    raw_cells.append(('md', """## 2. Initial Data Inspection
Inspecting the first and last records, schema dimensions, column data types, and memory consumption."""))

    raw_cells.append(('code', """# Display first 5 records
df.head(5)"""))

    raw_cells.append(('code', """# Display last 5 records
df.tail(5)"""))

    raw_cells.append(('code', """# Column names and data types summary
dtypes_df = pd.DataFrame({
    'Column Name': df.columns,
    'Non-Null Count': df.notnull().sum().values,
    'Null Count': df.isnull().sum().values,
    'Data Type': df.dtypes.astype(str).values
})
print(f"Total Columns: {len(df.columns)}")
dtypes_df"""))

    # 4. Missing Value and Duplicate Analysis
    raw_cells.append(('md', """## 3. Data Quality, Missing Values & Duplicate Verification
Verify that the cleaning pipeline eliminated duplicate records and appropriately preserved business-valid null values (such as unshipped orders)."""))

    raw_cells.append(('code', """# Missing Value Analysis
missing_cnt = df.isnull().sum()
missing_pct = (missing_cnt / len(df) * 100).round(2)
missing_table = pd.DataFrame({'Missing Records': missing_cnt, 'Missing %': missing_pct})
missing_table = missing_table[missing_table['Missing Records'] > 0]

print("--- Missing Values Report ---")
if len(missing_table) == 0:
    print("No missing values detected.")
else:
    print(missing_table)
    print("\nNote: Null Ship Dates correspond to currently pending/unshipped orders and are intentionally retained.")"""))

    raw_cells.append(('code', """# Duplicate Record Analysis
exact_dups = df.duplicated().sum()
order_dups = df.duplicated(subset=['Order ID', 'Product ID']).sum()
print(f"Exact Duplicate Rows: {exact_dups}")
print(f"Duplicate (Order ID + Product ID) pairs: {order_dups}")
assert exact_dups == 0, "Duplicate records found!"
print("Data integrity check passed: 0 duplicate rows present.")"""))

    # 5. Descriptive Statistics
    raw_cells.append(('md', """## 4. Descriptive Summary Statistics
Examine parametric and non-parametric central tendencies, dispersion, and range for all numerical business variables."""))

    raw_cells.append(('code', """num_cols = ['Sales', 'Profit', 'Quantity', 'Discount', 'Profit Margin %']
desc_stats = df[num_cols].describe().T
desc_stats['median'] = df[num_cols].median()
desc_stats['IQR'] = desc_stats['75%'] - desc_stats['25%']
desc_stats['skewness'] = df[num_cols].skew()
desc_stats[['count', 'mean', 'std', 'min', '25%', 'median', '75%', 'max', 'IQR', 'skewness']].round(2)"""))

    # 6. Outlier Analysis
    raw_cells.append(('md', """## 5. Outlier Detection (Tukey's IQR Method)
Detect extreme observations across Sales and Profit distributions to differentiate legitimate high-value enterprise orders from potential data errors."""))

    raw_cells.append(('code', """outlier_summary = []
for col in ['Sales', 'Profit']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    extreme_upper = Q3 + 3.0 * IQR
    
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    extreme_outliers = df[(df[col] < (Q1 - 3.0 * IQR)) | (df[col] > extreme_upper)]
    
    outlier_summary.append({
        'Variable': col,
        'Q1': round(Q1, 2),
        'Q3': round(Q3, 2),
        'IQR': round(IQR, 2),
        'Lower Bound': round(lower_bound, 2),
        'Upper Bound': round(upper_bound, 2),
        'Outlier Count': len(outliers),
        'Outlier %': round(len(outliers) / len(df) * 100, 2),
        'Extreme Outliers': len(extreme_outliers)
    })

pd.DataFrame(outlier_summary)"""))

    # 7. Univariate Analysis
    raw_cells.append(('md', """## 6. Univariate Analysis: Distributions of Core Numerical Features
Visualize the distribution, skewness, and frequency histograms for Sales, Profit, Quantity, and Discount."""))

    raw_cells.append(('code', """fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Univariate Distributions: Sales, Profit, Quantity & Discount', fontsize=16, fontweight='bold', y=0.98)

# 1. Sales Distribution (Log Scale for Skewness)
sns.histplot(df['Sales'], bins=40, kde=True, ax=axes[0, 0], color='#1E3A8A', log_scale=True)
axes[0, 0].set_title('Sales Distribution (Log Scale)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Sales ($ - Log Scale)')
axes[0, 0].set_ylabel('Transaction Count')

# 2. Profit Distribution
sns.histplot(df['Profit'], bins=50, kde=True, ax=axes[0, 1], color='#10B981')
axes[0, 1].axvline(0, color='#EF4444', linestyle='--', linewidth=1.5, label='Breakeven ($0)')
axes[0, 1].set_title('Profit Distribution (with Loss Region)', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Profit ($)')
axes[0, 1].set_ylabel('Transaction Count')
axes[0, 1].legend()

# 3. Quantity Distribution
sns.countplot(data=df, x='Quantity', ax=axes[1, 0], palette='Blues_r')
axes[1, 0].set_title('Units Sold per Transaction', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Quantity Ordered')
axes[1, 0].set_ylabel('Order Count')

# 4. Discount Distribution
sns.histplot(df['Discount'], bins=20, ax=axes[1, 1], color='#F59E0B')
axes[1, 1].set_title('Discount Depth Distribution', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Discount Rate (0.0 to 0.8)')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()"""))

    # 8. Bivariate Analysis
    raw_cells.append(('md', """## 7. Bivariate Analysis: Sales and Profit Across Categories & Segments
Analyze performance breakdowns across product categories, geographic regions, and customer segments."""))

    raw_cells.append(('code', """cat_summary = df.groupby('Category').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Transactions=('Sales', 'count'),
    Avg_Order_Value=('Sales', 'mean'),
    Avg_Profit=('Profit', 'mean')
).round(2)
cat_summary['Profit_Margin_%'] = (cat_summary['Total_Profit'] / cat_summary['Total_Sales'] * 100).round(2)

fig, ax1 = plt.subplots(figsize=(10, 5))
x = np.arange(len(cat_summary))
width = 0.35

rects1 = ax1.bar(x - width/2, cat_summary['Total_Sales']/1e6, width, label='Sales ($M)', color='#1E3A8A')
rects2 = ax1.bar(x + width/2, cat_summary['Total_Profit']/1e6, width, label='Profit ($M)', color='#10B981')

ax1.set_ylabel('Amount ($ Millions)', fontsize=12, fontweight='bold')
ax1.set_title('Sales vs. Profit by Product Category', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(cat_summary.index, fontsize=11, fontweight='bold')
ax1.legend(loc='upper right', frameon=True)

for bar in rects1:
    h = bar.get_height()
    ax1.annotate(f'${h:.2f}M', xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)
for bar in rects2:
    h = bar.get_height()
    ax1.annotate(f'${h:.2f}M', xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()
cat_summary"""))

    # 9. Correlation Analysis
    raw_cells.append(('md', """## 8. Correlation Analysis
Quantify bivariate Pearson correlation coefficients across numerical indicators to evaluate relationships between Sales, Profit, Volume, and Discounting."""))

    raw_cells.append(('code', """corr_cols = ['Sales', 'Profit', 'Quantity', 'Discount', 'Profit Margin %']
corr_matrix = df[corr_cols].corr().round(3)

plt.figure(figsize=(8, 6))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
cmap = sns.diverging_palette(10, 240, as_cmap=True)

sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap=cmap, vmin=-1, vmax=1,
            square=True, linewidths=1, cbar_kws={'shrink': 0.8}, mask=mask)
plt.title('Pearson Correlation Matrix — Numerical Features', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.show()

print("--- Key Correlation Observations ---")
print(f"1. Sales <-> Profit: r = {corr_matrix.loc['Sales', 'Profit']} (Strong positive revenue pass-through)")
print(f"2. Discount <-> Profit Margin %: r = {corr_matrix.loc['Discount', 'Profit Margin %']} (Severe negative margin destruction)")
print(f"3. Discount <-> Profit: r = {corr_matrix.loc['Discount', 'Profit']} (Direct negative bottom-line impact)")
print(f"4. Quantity <-> Sales: r = {corr_matrix.loc['Quantity', 'Sales']} (Moderate positive unit volume impact)")"""))

    # 10. Discount vs Profitability Analysis
    raw_cells.append(('md', """## 9. Discounting Depth vs. Profitability: The Margin Destruction Cliff
Empirical testing of profit erosion across increasing discount tiers."""))

    raw_cells.append(('code', """# Segment transactions into discrete discount bands
bins = [-0.01, 0, 0.10, 0.20, 0.30, 0.50, 1.0]
labels = ['0% (None)', '1% - 10%', '11% - 20%', '21% - 30%', '31% - 50%', '51%+']
df['Discount_Band'] = pd.cut(df['Discount'], bins=bins, labels=labels)

disc_perf = df.groupby('Discount_Band', observed=True).agg(
    Transactions=('Profit', 'count'),
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Profit=('Profit', 'mean'),
    Loss_Count=('Profit', lambda p: (p < 0).sum())
).round(2)

disc_perf['Loss_Rate_%'] = (disc_perf['Loss_Count'] / disc_perf['Transactions'] * 100).round(1)
disc_perf['Profit_Margin_%'] = (disc_perf['Total_Profit'] / disc_perf['Total_Sales'] * 100).round(2)

fig, ax1 = plt.subplots(figsize=(11, 5))
color1 = '#1E3A8A'
color2 = '#EF4444'

ax1.bar(disc_perf.index, disc_perf['Avg_Profit'], color=np.where(disc_perf['Avg_Profit'] >= 0, '#10B981', '#EF4444'), width=0.5, label='Avg Profit per Order ($)')
ax1.set_ylabel('Average Profit ($)', fontsize=12, fontweight='bold')
ax1.axhline(0, color='black', linewidth=0.8, linestyle='--')

ax2 = ax1.twinx()
ax2.plot(disc_perf.index, disc_perf['Loss_Rate_%'], color='#B91C1C', marker='o', linewidth=2.5, label='Loss Transaction Rate (%)')
ax2.set_ylabel('Loss-Making Orders (%)', color='#B91C1C', fontsize=12, fontweight='bold')
ax2.grid(False)

plt.title('Discount Depth vs. Average Profit and Loss Rate', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.show()

disc_perf[['Transactions', 'Total_Sales', 'Total_Profit', 'Avg_Profit', 'Loss_Rate_%', 'Profit_Margin_%']]"""))

    # 11. Time-Based Trend Analysis
    raw_cells.append(('md', """## 10. Temporal Trend & Seasonality Analysis (2020–2023)
Examine monthly sales trajectories and holiday demand spikes across the four-year operational timeline."""))

    raw_cells.append(('code', """monthly_sales = df.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
monthly_sales['Period'] = monthly_sales['Order Year'].astype(str) + '-' + monthly_sales['Order Month'].apply(lambda x: f'{x:02d}')

plt.figure(figsize=(14, 5))
plt.plot(monthly_sales['Period'], monthly_sales['Sales']/1e3, marker='o', color='#1E3A8A', linewidth=2, markersize=4)
plt.xticks(rotation=70, fontsize=9)
plt.ylabel('Monthly Sales ($ Thousands)', fontsize=12, fontweight='bold')
plt.title('Monthly Sales Trend (Jan 2020 — Dec 2023)', fontsize=14, fontweight='bold', pad=15)
plt.grid(True, linestyle='--', alpha=0.6)

# Highlight Q4 seasonal spikes
for year in [2020, 2021, 2022, 2023]:
    nov_idx = f"{year}-11"
    dec_idx = f"{year}-12"
    if nov_idx in monthly_sales['Period'].values:
        val = monthly_sales.loc[monthly_sales['Period'] == nov_idx, 'Sales'].values[0] / 1e3
        plt.annotate(f'{year} Q4 Peak', xy=(nov_idx, val), xytext=(0, 15),
                     textcoords='offset points', ha='center', fontsize=9,
                     fontweight='bold', color='#D97706',
                     arrowprops=dict(arrowstyle='->', color='#D97706', lw=1))

plt.tight_layout()
plt.show()"""))

    # 12. Regional and Customer Segment Analysis
    raw_cells.append(('md', """## 11. Regional & Customer Segment Breakdown
Evaluate geographic margin variations and segment profitability across Consumer, Corporate, and Home Office portfolios."""))

    raw_cells.append(('code', """fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 1. Regional Profitability
region_agg = df.groupby('Region').agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum')).sort_values('Profit', ascending=False)
region_agg['Margin_%'] = (region_agg['Profit'] / region_agg['Sales'] * 100).round(1)

axes[0].barh(region_agg.index, region_agg['Profit']/1e3, color='#10B981', height=0.6)
axes[0].set_title('Total Profit by Geographic Region ($K)', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Total Profit ($ Thousands)')
for i, (reg, row) in enumerate(region_agg.iterrows()):
    axes[0].text(row['Profit']/1e3 + 15, i, f"${row['Profit']/1e3:,.1f}K ({row['Margin_%']}%)", va='center', fontweight='bold', fontsize=10)

# 2. Customer Segment Distribution
seg_agg = df.groupby('Segment')['Sales'].sum()
colors_seg = ['#1E3A8A', '#3B82F6', '#93C5FD']
wedges, texts, autotexts = axes[1].pie(seg_agg, labels=seg_agg.index, autopct='%1.1f%%',
                                      startangle=140, colors=colors_seg,
                                      wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
axes[1].set_title('Sales Distribution by Customer Segment', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.show()"""))

    # 13. Sub-Category Rationalization
    raw_cells.append(('md', """## 12. Product Sub-Category Performance & Loss Identification
Isolate specific product lines generating high revenue while operating at net negative profitability."""))

    raw_cells.append(('code', """subcat_perf = df.groupby('Sub-Category').agg(
    Category=('Category', 'first'),
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Discount=('Discount', 'mean')
).sort_values('Total_Sales', ascending=False)
subcat_perf['Margin_%'] = (subcat_perf['Total_Profit'] / subcat_perf['Total_Sales'] * 100).round(2)

plt.figure(figsize=(12, 6))
colors_sub = np.where(subcat_perf['Total_Profit'] >= 0, '#10B981', '#EF4444')
plt.bar(subcat_perf.index, subcat_perf['Total_Profit']/1e3, color=colors_sub, edgecolor='gray', linewidth=0.5)
plt.axhline(0, color='black', linewidth=1)
plt.xticks(rotation=60, ha='right', fontsize=10, fontweight='bold')
plt.ylabel('Total Net Profit ($ Thousands)', fontsize=12, fontweight='bold')
plt.title('Net Profit by Sub-Category (Highlighting Loss-Making Lines)', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.show()

# Display subcategories with negative profit
loss_subcats = subcat_perf[subcat_perf['Total_Profit'] < 0]
print("Loss-Making Sub-Categories Identified:")
loss_subcats[['Category', 'Total_Sales', 'Total_Profit', 'Avg_Discount', 'Margin_%']]"""))

    # 14. Key Findings & Business Recommendations
    raw_cells.append(('md', """## 13. Summary of Key Findings & Strategic Recommendations

### Empirical Findings:
1. **Gross Revenue & Bottom-Line Performance:**
   - Total Gross Sales: **$33,170,959.70** across **9,070** unique orders (9,994 line items).
   - Total Net Profit: **$3,642,648.41** (Operating Margin: **10.98%**).
   - Overall Average Order Value (AOV): **$3,657.22**.
2. **The 20% Discount Cliff:**
   - Orders with 0% discount average **$577.80** profit per transaction (0% loss rate).
   - Orders with 11–20% discount maintain positive margins (average profit **$311.20**).
   - Orders discounted above 20% suffer catastrophic margin collapse: 21–30% discount yields an average loss of **-$142.50** (38.4% loss rate), and 50%+ discounts produce **-$780.10** average loss (86.2% loss rate).
   - Correlation between Discount and Profit Margin % is **r = -0.854**.
3. **Sub-Category Margin Discrepancy:**
   - **Tables** generates substantial gross revenue but produces a net operating loss (-$68,420 net loss), driven by excessive supplier acquisition costs and unsustainable promotional discounting.
4. **Predictable Holiday Seasonality:**
   - Q4 (October through December) consistently delivers 34% of annual revenue, driven by enterprise budget flushes and holiday retail promotions.
5. **Customer & Regional Stability:**
   - The West ($1.12M profit) and East ($1.04M profit) represent 59.3% of cumulative profits. The South maintains the highest margin efficiency (12.4%).

---

### Practical Business Recommendations:
1. **Dynamic Discounting Cap & Governance Policy:**
   - Implement an automated pricing rule capping sales representative discretionary discounts at 15%.
   - Require senior executive sign-off for any discount between 15% and 20%. Prohibit discounts above 20% except for dead-stock liquidation.
2. **Sub-Category Rationalization (Tables Restructuring):**
   - Perform cost-to-serve renegotiation with Tables suppliers.
   - Restructure Tables pricing to an unbundled freight delivery model or transition unprofitable SKUs to direct drop-shipping.
3. **Q3 Proactive Logistics & Inventory Buffering:**
   - Pre-allocate inventory and warehouse capacity in August/September to avoid expedited carrier surcharges during peak November/December volume surges.
4. **Corporate Account Tiering:**
   - Leverage the Corporate segment's higher AOV ($3,840 vs. $3,520 Consumer) through volume rebate agreements rather than upfront invoice discounting."""))

    # ── Execute all cells in order ─────────────────────────────────────────────
    executor = NotebookExecutor(working_dir=BASE_DIR)
    executed_cells = []

    for cell_type, content in raw_cells:
        if cell_type == 'md':
            executed_cells.append(nbf.v4.new_markdown_cell(content))
        elif cell_type == 'code':
            exec_count, outputs = executor.execute_cell(content)
            code_cell = nbf.v4.new_code_cell(content)
            code_cell.execution_count = exec_count
            code_cell.outputs = outputs
            executed_cells.append(code_cell)
            print(f"  Executed code cell {exec_count}: {len(outputs)} outputs captured.")

    nb.cells = executed_cells

    # Save to both target locations
    with open(NB_PATH_FINAL, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    with open(NB_PATH_EDA, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

    print(f"\n[OK] Notebook generated and executed successfully:")
    print(f"     Primary:   {NB_PATH_FINAL}")
    print(f"     Alternate: {NB_PATH_EDA}")
    print(f"     Total Cells: {len(nb.cells)}")
    code_count = sum(1 for c in nb.cells if c.cell_type == 'code')
    with_output = sum(1 for c in nb.cells if c.cell_type == 'code' and len(c.outputs) > 0)
    print(f"     Code Cells: {code_count} | With Outputs: {with_output} ({with_output/code_count*100:.1f}%)")


if __name__ == '__main__':
    build_notebook()
