"""
eda_analysis.py
---------------
Phase 4 & 5: Exploratory Data Analysis and Visualizations
E-Commerce Sales Analysis Project — Week 6 Internship Assignment

This script performs comprehensive EDA and generates all required
visualizations from the cleaned dataset.

Usage:
    python src/eda_analysis.py

Outputs:
    visualizations/*.png  (8+ charts)
    reports/eda_summary.md
"""

import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime

warnings.filterwarnings('ignore')

# ── Path Configuration ─────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, 'data', 'cleaned_sales.csv')
VIZ_DIR = os.path.join(BASE_DIR, 'visualizations')
REPORT_PATH = os.path.join(BASE_DIR, 'reports', 'eda_summary.md')

os.makedirs(VIZ_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'reports'), exist_ok=True)

# ── Plot Styling ───────────────────────────────────────────────────────────────
PALETTE = ['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0',
           '#00BCD4', '#FF5722', '#607D8B', '#8BC34A', '#795548']
BLUE = '#2196F3'
GREEN = '#4CAF50'
ORANGE = '#FF9800'
RED = '#F44336'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

eda_log = []


def log(msg):
    eda_log.append(msg)
    print(msg)


def save_chart(fig, filename, desc=""):
    path = os.path.join(VIZ_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    log(f"[SAVED] {filename}: {desc}")
    return path


def fmt_dollar(x, pos=None):
    if x >= 1_000_000:
        return f'${x/1_000_000:.1f}M'
    elif x >= 1_000:
        return f'${x/1_000:.0f}K'
    return f'${x:.0f}'


# ══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════
def load_data():
    log("Loading cleaned dataset...")
    df = pd.read_csv(CLEAN_DATA_PATH)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    if 'Ship Date' in df.columns:
        df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    log(f"Loaded: {df.shape[0]:,} rows x {df.shape[1]} columns")
    return df


# ══════════════════════════════════════════════════════════════════════════════
# DESCRIPTIVE STATISTICS
# ══════════════════════════════════════════════════════════════════════════════
def descriptive_statistics(df):
    log("\n=== DESCRIPTIVE STATISTICS ===")
    num_cols = ['Sales', 'Profit', 'Quantity', 'Discount', 'Profit Margin %']
    num_cols = [c for c in num_cols if c in df.columns]
    stats = df[num_cols].describe().T
    stats['median'] = df[num_cols].median()
    log(str(stats.round(2)))

    log("\n=== CATEGORICAL FREQUENCY TABLES ===")
    for col in ['Category', 'Segment', 'Region', 'Ship Mode']:
        if col in df.columns:
            freq = df[col].value_counts()
            log(f"\n{col}:\n{freq}")

    return stats


# ══════════════════════════════════════════════════════════════════════════════
# BUSINESS KPIs
# ══════════════════════════════════════════════════════════════════════════════
def compute_kpis(df):
    kpis = {
        'total_sales': df['Sales'].sum(),
        'total_profit': df['Profit'].sum(),
        'total_quantity': int(df['Quantity'].sum()),
        'total_orders': df['Order ID'].nunique(),
        'total_customers': df['Customer ID'].nunique(),
        'profit_margin_pct': (df['Profit'].sum() / df['Sales'].sum() * 100),
        'avg_order_value': df.groupby('Order ID')['Sales'].sum().mean(),
    }
    log("\n=== KEY PERFORMANCE INDICATORS ===")
    log(f"  Total Sales:       ${kpis['total_sales']:,.2f}")
    log(f"  Total Profit:      ${kpis['total_profit']:,.2f}")
    log(f"  Total Quantity:    {kpis['total_quantity']:,} units")
    log(f"  Total Orders:      {kpis['total_orders']:,}")
    log(f"  Unique Customers:  {kpis['total_customers']:,}")
    log(f"  Profit Margin:     {kpis['profit_margin_pct']:.2f}%")
    log(f"  Avg Order Value:   ${kpis['avg_order_value']:,.2f}")
    return kpis


# ══════════════════════════════════════════════════════════════════════════════
# CHART 1: Sales by Category — Bar Chart
# ══════════════════════════════════════════════════════════════════════════════
def chart_sales_by_category(df):
    sales_cat = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(sales_cat.index, sales_cat.values,
                  color=[BLUE, GREEN, ORANGE], edgecolor='white', linewidth=1.5, width=0.5)

    for bar, val in zip(bars, sales_cat.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20000,
                fmt_dollar(val), ha='center', va='bottom', fontweight='bold', fontsize=12)

    ax.set_title('Total Sales by Product Category', fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Total Sales (USD)', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    ax.legend(['Sales'], loc='upper right')

    return save_chart(fig, '01_sales_by_category.png',
                      'Total sales grouped by product category')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 2: Monthly Sales Trend — Line Chart
# ══════════════════════════════════════════════════════════════════════════════
def chart_monthly_sales_trend(df):
    df['YearMonth'] = df['Order Date'].dt.to_period('M')
    monthly = df.groupby('YearMonth')['Sales'].sum().reset_index()
    monthly['YearMonth_dt'] = monthly['YearMonth'].dt.to_timestamp()

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(monthly['YearMonth_dt'], monthly['Sales'],
            color=BLUE, linewidth=2.2, marker='o', markersize=3, alpha=0.9)
    ax.fill_between(monthly['YearMonth_dt'], monthly['Sales'],
                    alpha=0.15, color=BLUE)

    ax.set_title('Monthly Sales Trend (Jan 2020 – Dec 2023)', fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Monthly Sales (USD)', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))

    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=45, ha='right')

    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')

    return save_chart(fig, '02_monthly_sales_trend.png',
                      'Monthly sales trend across 4 years')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 3: Profit by Region — Horizontal Bar Chart
# ══════════════════════════════════════════════════════════════════════════════
def chart_profit_by_region(df):
    profit_region = df.groupby('Region')['Profit'].sum().sort_values(ascending=True)
    colors = [GREEN if v >= 0 else RED for v in profit_region.values]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(profit_region.index, profit_region.values,
                   color=colors, edgecolor='white', linewidth=1.2, height=0.5)

    for bar, val in zip(bars, profit_region.values):
        label_x = val + (abs(profit_region.max()) * 0.01)
        ax.text(label_x, bar.get_y() + bar.get_height()/2,
                fmt_dollar(val), va='center', fontweight='bold', fontsize=11)

    ax.set_title('Total Profit by Region', fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel('Total Profit (USD)', fontsize=12)
    ax.set_ylabel('Region', fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.axvline(0, color='grey', linestyle='--', linewidth=1)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')

    return save_chart(fig, '03_profit_by_region.png',
                      'Total profit by geographic region')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 4: Sales by Customer Segment — Donut Chart
# ══════════════════════════════════════════════════════════════════════════════
def chart_sales_by_segment(df):
    seg_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Donut
    wedges, texts, autotexts = ax1.pie(
        seg_sales.values,
        labels=seg_sales.index,
        autopct='%1.1f%%',
        colors=[BLUE, GREEN, ORANGE],
        startangle=90,
        wedgeprops={'width': 0.55, 'edgecolor': 'white', 'linewidth': 2},
        pctdistance=0.75
    )
    for at in autotexts:
        at.set_fontsize(12)
        at.set_fontweight('bold')

    ax1.set_title('Sales Share by\nCustomer Segment', fontsize=13, fontweight='bold')

    # Bar
    bars = ax2.bar(seg_sales.index, seg_sales.values,
                   color=[BLUE, GREEN, ORANGE], edgecolor='white', linewidth=1.5, width=0.4)
    for bar, val in zip(bars, seg_sales.values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15000,
                 fmt_dollar(val), ha='center', va='bottom', fontweight='bold', fontsize=11)

    ax2.set_title('Total Sales by\nCustomer Segment', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Total Sales (USD)', fontsize=11)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax2.set_facecolor('#F8F9FA')

    fig.suptitle('Customer Segment Performance Analysis', fontsize=15, fontweight='bold', y=1.02)
    fig.patch.set_facecolor('white')
    plt.tight_layout()

    return save_chart(fig, '04_sales_by_segment.png',
                      'Sales distribution across customer segments')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 5: Discount vs Profit — Scatter Plot
# ══════════════════════════════════════════════════════════════════════════════
def chart_discount_vs_profit(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    categories = df['Category'].unique()
    cat_colors = dict(zip(categories, [BLUE, GREEN, ORANGE]))

    for cat in categories:
        mask = df['Category'] == cat
        ax.scatter(df.loc[mask, 'Discount'],
                   df.loc[mask, 'Profit'],
                   c=cat_colors[cat], label=cat,
                   alpha=0.4, s=20, edgecolors='none')

    # Trend line
    x = df['Discount'].values
    y = df['Profit'].values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    x_line = np.linspace(x.min(), x.max(), 100)
    ax.plot(x_line, p(x_line), 'r--', linewidth=2, label='Trend Line', zorder=5)

    ax.axhline(0, color='grey', linestyle=':', linewidth=1.2)
    ax.set_title('Discount vs. Profit Relationship', fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel('Discount Rate', fontsize=12)
    ax.set_ylabel('Profit (USD)', fontsize=12)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.legend(title='Category', fontsize=10)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')

    corr = np.corrcoef(x, y)[0, 1]
    ax.text(0.05, 0.97, f'Correlation: {corr:.3f}',
            transform=ax.transAxes, va='top', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    return save_chart(fig, '05_discount_vs_profit.png',
                      'Scatter plot showing discount vs profit relationship')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 6: Correlation Heatmap
# ══════════════════════════════════════════════════════════════════════════════
def chart_correlation_heatmap(df):
    num_cols = ['Sales', 'Profit', 'Quantity', 'Discount', 'Profit Margin %']
    num_cols = [c for c in num_cols if c in df.columns]
    corr_matrix = df[num_cols].corr()

    log("\n=== CORRELATION MATRIX ===")
    log(str(corr_matrix.round(3)))

    fig, ax = plt.subplots(figsize=(9, 7))
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.3f',
        cmap='RdYlGn',
        center=0,
        vmin=-1, vmax=1,
        square=True,
        linewidths=0.5,
        linecolor='white',
        ax=ax,
        annot_kws={'size': 12, 'weight': 'bold'},
        cbar_kws={'shrink': 0.8}
    )
    ax.set_title('Correlation Matrix — Numerical Variables', fontsize=14, fontweight='bold', pad=15)
    plt.xticks(rotation=30, ha='right')
    plt.yticks(rotation=0)
    fig.patch.set_facecolor('white')

    return save_chart(fig, '06_correlation_heatmap.png',
                      'Correlation matrix for numerical variables')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 7: Top 10 Products by Sales — Horizontal Bar Chart
# ══════════════════════════════════════════════════════════════════════════════
def chart_top10_products(df):
    top10 = df.groupby('Product Name')['Sales'].sum().nlargest(10).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(11, 7))
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(top10)))
    bars = ax.barh(range(len(top10)), top10.values,
                   color=colors, edgecolor='white', linewidth=1.2, height=0.65)

    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels([name[:40] + '...' if len(name) > 40 else name
                        for name in top10.index], fontsize=10)

    for bar, val in zip(bars, top10.values):
        ax.text(val + top10.max() * 0.01, bar.get_y() + bar.get_height()/2,
                fmt_dollar(val), va='center', fontweight='bold', fontsize=10)

    ax.set_title('Top 10 Products by Total Sales', fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel('Total Sales (USD)', fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    plt.tight_layout()

    return save_chart(fig, '07_top10_products.png',
                      'Top 10 products by total revenue')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 8: Sales and Profit by Sub-Category — Comparative Chart
# ══════════════════════════════════════════════════════════════════════════════
def chart_sales_profit_subcategory(df):
    subcat = df.groupby('Sub-Category').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).sort_values('Sales', ascending=True)

    fig, ax = plt.subplots(figsize=(12, 9))
    y = np.arange(len(subcat))
    height = 0.35

    bars1 = ax.barh(y + height/2, subcat['Sales'], height,
                    label='Sales', color=BLUE, alpha=0.85, edgecolor='white')
    bars2 = ax.barh(y - height/2, subcat['Profit'], height,
                    label='Profit', color=GREEN, alpha=0.85, edgecolor='white')

    # Color profit bars red where negative
    for bar, val in zip(bars2, subcat['Profit']):
        if val < 0:
            bar.set_color(RED)

    ax.set_yticks(y)
    ax.set_yticklabels(subcat.index, fontsize=10)
    ax.axvline(0, color='grey', linestyle='--', linewidth=1)
    ax.set_title('Sales and Profit by Sub-Category', fontsize=15, fontweight='bold', pad=15)
    ax.set_xlabel('Amount (USD)', fontsize=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.legend(fontsize=11, loc='lower right')
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')
    plt.tight_layout()

    return save_chart(fig, '08_sales_profit_subcategory.png',
                      'Comparative sales and profit by sub-category')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 9: Yearly Sales Comparison
# ══════════════════════════════════════════════════════════════════════════════
def chart_yearly_comparison(df):
    yearly = df.groupby('Order Year').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for ax, col, color, title in zip(
        axes,
        ['Sales', 'Profit', 'Orders'],
        [BLUE, GREEN, ORANGE],
        ['Total Sales by Year', 'Total Profit by Year', 'Unique Orders by Year']
    ):
        bars = ax.bar(yearly['Order Year'].astype(str), yearly[col],
                      color=color, alpha=0.85, edgecolor='white', linewidth=1.5, width=0.5)
        for bar, val in zip(bars, yearly[col]):
            label = f"{val/1000:.0f}K" if col in ['Sales', 'Profit'] else f"{val:,.0f}"
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + yearly[col].max()*0.02,
                    label, ha='center', va='bottom', fontweight='bold', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('Year', fontsize=10)
        if col in ['Sales', 'Profit']:
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
        ax.set_facecolor('#F8F9FA')

    fig.suptitle('Year-over-Year Performance Summary (2020–2023)',
                 fontsize=14, fontweight='bold', y=1.02)
    fig.patch.set_facecolor('white')
    plt.tight_layout()

    return save_chart(fig, '09_yearly_comparison.png',
                      'Year-over-year sales, profit, and order trends')


# ══════════════════════════════════════════════════════════════════════════════
# CHART 10: Profit Distribution — Box Plots by Category
# ══════════════════════════════════════════════════════════════════════════════
def chart_profit_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    cats = df['Category'].unique()
    data_by_cat = [df.loc[df['Category'] == c, 'Profit'].values for c in cats]

    bp = ax.boxplot(data_by_cat, tick_labels=cats, patch_artist=True,
                    notch=False, showfliers=True,
                    flierprops=dict(marker='o', markersize=3, alpha=0.3))

    colors = [BLUE, GREEN, ORANGE]
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.axhline(0, color='red', linestyle='--', linewidth=1.2, label='Break-even')
    ax.set_title('Profit Distribution by Category (Box Plot)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Profit per Transaction (USD)', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_dollar))
    ax.legend(fontsize=10)
    ax.set_facecolor('#F8F9FA')
    fig.patch.set_facecolor('white')

    return save_chart(fig, '10_profit_distribution.png',
                      'Profit distribution and outliers by category')


# ══════════════════════════════════════════════════════════════════════════════
# GENERATE EDA REPORT
# ══════════════════════════════════════════════════════════════════════════════
def generate_eda_report(df, kpis, stats):
    cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    cat_profit = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=False)
    seg_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)

    report = f"""# Exploratory Data Analysis Summary
## E-Commerce Sales Analysis Project — Week 6 Internship Assignment

**Generated:** {datetime.now().strftime("%B %d, %Y at %H:%M")}  
**Dataset:** Synthetic Sample Superstore-style data (labeled as SYNTHETIC)  
**Rows Analyzed:** {len(df):,}

---

## Key Performance Indicators

| KPI | Value |
|-----|-------|
| Total Sales | ${kpis['total_sales']:,.2f} |
| Total Profit | ${kpis['total_profit']:,.2f} |
| Total Quantity Sold | {kpis['total_quantity']:,} units |
| Total Orders (Unique) | {kpis['total_orders']:,} |
| Unique Customers | {kpis['total_customers']:,} |
| Overall Profit Margin | {kpis['profit_margin_pct']:.2f}% |
| Average Order Value | ${kpis['avg_order_value']:,.2f} |

## Sales by Category

| Category | Total Sales | Total Profit |
|----------|------------|--------------|
"""
    for cat in cat_sales.index:
        report += f"| {cat} | ${cat_sales[cat]:,.2f} | ${cat_profit.get(cat, 0):,.2f} |\n"

    report += f"""
## Regional Performance

| Region | Total Sales | Total Profit |
|--------|------------|--------------|
"""
    region_profit_series = df.groupby('Region')['Profit'].sum()
    for reg in region_sales.index:
        report += f"| {reg} | ${region_sales[reg]:,.2f} | ${region_profit_series.get(reg, 0):,.2f} |\n"

    report += f"""
## Customer Segment Performance

| Segment | Total Sales |
|---------|------------|
"""
    for seg in seg_sales.index:
        report += f"| {seg} | ${seg_sales[seg]:,.2f} |\n"

    report += f"""
## Descriptive Statistics

| Metric | Sales | Profit | Quantity | Discount |
|--------|-------|--------|----------|---------|
| Mean | ${df['Sales'].mean():,.2f} | ${df['Profit'].mean():,.2f} | {df['Quantity'].mean():.2f} | {df['Discount'].mean():.3f} |
| Median | ${df['Sales'].median():,.2f} | ${df['Profit'].median():,.2f} | {df['Quantity'].median():.1f} | {df['Discount'].median():.3f} |
| Std Dev | ${df['Sales'].std():,.2f} | ${df['Profit'].std():,.2f} | {df['Quantity'].std():.2f} | {df['Discount'].std():.3f} |
| Min | ${df['Sales'].min():,.2f} | ${df['Profit'].min():,.2f} | {df['Quantity'].min()} | {df['Discount'].min():.2f} |
| Max | ${df['Sales'].max():,.2f} | ${df['Profit'].max():,.2f} | {df['Quantity'].max()} | {df['Discount'].max():.2f} |
| Q25 | ${df['Sales'].quantile(0.25):,.2f} | ${df['Profit'].quantile(0.25):,.2f} | {df['Quantity'].quantile(0.25):.1f} | {df['Discount'].quantile(0.25):.2f} |
| Q75 | ${df['Sales'].quantile(0.75):,.2f} | ${df['Profit'].quantile(0.75):,.2f} | {df['Quantity'].quantile(0.75):.1f} | {df['Discount'].quantile(0.75):.2f} |

## Correlation Analysis

The correlation matrix reveals:
- **Sales and Profit**: Strong positive correlation — higher sales generally lead to higher profits
- **Discount and Profit**: Negative correlation — higher discounts reduce profitability
- **Quantity and Sales**: Moderate positive correlation — more units = more revenue

## Charts Generated

| # | Chart File | Description |
|---|-----------|-------------|
| 1 | 01_sales_by_category.png | Sales by product category |
| 2 | 02_monthly_sales_trend.png | Monthly sales trend 2020-2023 |
| 3 | 03_profit_by_region.png | Profit by geographic region |
| 4 | 04_sales_by_segment.png | Sales by customer segment |
| 5 | 05_discount_vs_profit.png | Discount vs profit scatter |
| 6 | 06_correlation_heatmap.png | Correlation matrix heatmap |
| 7 | 07_top10_products.png | Top 10 products by sales |
| 8 | 08_sales_profit_subcategory.png | Sales and profit by sub-category |
| 9 | 09_yearly_comparison.png | Year-over-year comparison |
| 10 | 10_profit_distribution.png | Profit distribution box plots |

---
*Generated by `src/eda_analysis.py`*
"""
    return report


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    log("=" * 60)
    log("E-COMMERCE SALES EDA & VISUALIZATIONS — WEEK 6 ASSIGNMENT")
    log("=" * 60)

    df = load_data()
    stats = descriptive_statistics(df)
    kpis = compute_kpis(df)

    log("\n=== GENERATING CHARTS ===")
    chart_sales_by_category(df)
    chart_monthly_sales_trend(df)
    chart_profit_by_region(df)
    chart_sales_by_segment(df)
    chart_discount_vs_profit(df)
    chart_correlation_heatmap(df)
    chart_top10_products(df)
    chart_sales_profit_subcategory(df)
    chart_yearly_comparison(df)
    chart_profit_distribution(df)

    # Save EDA report
    report_text = generate_eda_report(df, kpis, stats)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_text)
    log(f"\n[SAVED] EDA summary: {REPORT_PATH}")

    log("\n" + "=" * 60)
    log("EDA AND VISUALIZATIONS COMPLETE — 10 charts generated.")
    log("=" * 60)


if __name__ == '__main__':
    main()
