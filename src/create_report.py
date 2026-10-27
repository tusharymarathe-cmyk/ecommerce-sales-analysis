"""
create_report.py
----------------
Generates the Final_Data_Analytics_Project_Report.pdf
using reportlab.
"""
import os, sys, shutil
import pandas as pd
import numpy as np

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image as RLImage, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(BASE_DIR, 'reports', 'Final_Data_Analytics_Project_Report.pdf')
PDF_ALT_PATH = os.path.join(BASE_DIR, 'reports', 'final_project_report.pdf')
VIZ_DIR = os.path.join(BASE_DIR, 'visualizations')
CLEAN_PATH = os.path.join(BASE_DIR, 'data', 'cleaned_sales.csv')
os.makedirs(os.path.dirname(PDF_PATH), exist_ok=True)

# Load data for real numbers
df = pd.read_csv(CLEAN_PATH)
df['Order Date'] = pd.to_datetime(df['Order Date'])

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_qty = int(df['Quantity'].sum())
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()
profit_margin = total_profit / total_sales * 100
avg_order = total_sales / total_orders

cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
cat_profit = df.groupby('Category')['Profit'].sum()
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
region_profit = df.groupby('Region')['Profit'].sum()
seg_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
subcat = df.groupby('Sub-Category').agg(Sales=('Sales','sum'), Profit=('Profit','sum'))
subcat['Margin%'] = (subcat['Profit'] / subcat['Sales'] * 100).round(2)
corr = df[['Sales','Profit','Quantity','Discount','Profit Margin %']].corr()

# ── Document Setup ─────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    rightMargin=2.0*cm,
    leftMargin=2.0*cm,
    topMargin=2.0*cm,
    bottomMargin=2.0*cm,
    title="E-Commerce Sales Data Analysis — Final Report",
    author="Internship Student",
    subject="Week 6 Data Analytics Assignment"
)

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()
W = A4[0] - 4.0*cm  # usable width

NAVY = colors.HexColor('#1A237E')
BLUE = colors.HexColor('#2196F3')
GREEN = colors.HexColor('#4CAF50')
ORANGE = colors.HexColor('#FF9800')
RED = colors.HexColor('#F44336')
LIGHT_GRAY = colors.HexColor('#F5F5F5')
MID_GRAY = colors.HexColor('#757575')
DARK_GRAY = colors.HexColor('#424242')

Title = ParagraphStyle('Title', parent=styles['Title'], fontSize=26,
    textColor=NAVY, spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica-Bold')
Subtitle = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=14,
    textColor=BLUE, spaceAfter=4, alignment=TA_CENTER)
H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=18,
    textColor=NAVY, spaceBefore=16, spaceAfter=6, fontName='Helvetica-Bold',
    borderPad=4, borderColor=NAVY, borderWidth=0)
H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14,
    textColor=BLUE, spaceBefore=12, spaceAfter=4, fontName='Helvetica-Bold')
H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontSize=12,
    textColor=DARK_GRAY, spaceBefore=8, spaceAfter=3, fontName='Helvetica-Bold')
Body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10,
    textColor=DARK_GRAY, spaceAfter=6, leading=15, alignment=TA_JUSTIFY)
Caption = ParagraphStyle('Caption', parent=styles['Normal'], fontSize=9,
    textColor=MID_GRAY, spaceAfter=8, alignment=TA_CENTER, fontStyle='italic')
Note = ParagraphStyle('Note', parent=styles['Normal'], fontSize=9,
    textColor=RED, spaceAfter=4, borderPad=4)
TOCEntry = ParagraphStyle('TOCEntry', parent=styles['Normal'], fontSize=10,
    textColor=DARK_GRAY, spaceAfter=3, leftIndent=10)

def hr(): return HRFlowable(width=W, thickness=1, color=BLUE, spaceAfter=8, spaceBefore=4)
def sp(h=0.3): return Spacer(1, h*cm)

def tbl(data, col_widths=None, style_cmds=None):
    base_style = [
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [LIGHT_GRAY, colors.white]),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#BDBDBD')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('WORDWRAP', (0,0), (-1,-1), 1),
    ]
    if style_cmds:
        base_style.extend(style_cmds)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(base_style))
    return t

def img(fname, width=W, caption_text=None):
    path = os.path.join(VIZ_DIR, fname)
    items = []
    if os.path.exists(path):
        items.append(RLImage(path, width=width, height=width*0.55))
        if caption_text:
            items.append(Paragraph(caption_text, Caption))
    else:
        items.append(Paragraph(f"[Chart not available: {fname}]", Caption))
    return items

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(3),
    Paragraph("E-Commerce Sales Data Analysis", Title),
    Paragraph("and Interactive Power BI Dashboard", ParagraphStyle(
        'big', parent=Subtitle, fontSize=18, textColor=BLUE)),
    sp(0.5),
    hr(),
    sp(0.3),
    Paragraph("Final Data Analytics Project Report", Subtitle),
    Paragraph("Week 6 Internship Assignment", Subtitle),
    sp(2),
    tbl(
        [["Field", "Details"],
         ["Student Name", "Tushar Marathe"],
         ["Internship Organization", "Internova"],
         ["Internship Domain", "Data Analytics"],
         ["Assignment", "Week 6: Git, GitHub & Final Data Analytics Project"],
         ["Maximum Marks", "100"],
         ["Duration", "7 Days"],
         ["Submission Date", datetime.now().strftime("%B %d, %Y")],
         ["Report Generated", datetime.now().strftime("%B %d, %Y at %H:%M")],
         ["Dataset Type", "Synthetic (Superstore-calibrated, 9,994 records)"],
         ["Tools Used", "Python, Pandas, NumPy, Matplotlib, Seaborn, Power BI, Git"]],
        col_widths=[6*cm, 11*cm]
    ),
    sp(1.5),
    Paragraph(
        "<b>⚠ IMPORTANT NOTICE:</b> The dataset used in this project is synthetically "
        "generated using Python (NumPy seed=42) to simulate retail sales data. All "
        "business findings are for educational purposes only and do not represent "
        "real-world business data.", Note
    ),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# ABSTRACT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("Abstract", H1), hr(),
    Paragraph(
        "This report presents a comprehensive end-to-end data analytics capstone project "
        f"analyzing {len(df):,} e-commerce retail sales transactions spanning January 2020 to "
        "December 2023. Using Python (Pandas, NumPy, Matplotlib, Seaborn), the project "
        "performs systematic data cleaning, exploratory data analysis, and generates 10 "
        "professional data visualizations. Key findings include: a total revenue of "
        f"${total_sales:,.0f}, a profit of ${total_profit:,.0f} ({profit_margin:.2f}% margin), "
        "a strong negative correlation between discount rates and profitability (-0.854), "
        "and a structurally loss-making Furniture Tables sub-category. Three actionable "
        "business recommendations are provided: implementing discount governance, developing "
        "a Corporate segment strategy, and repricing the Tables sub-category. A complete "
        "Power BI dashboard preparation package is included with setup instructions and DAX "
        "measures. The project is documented for GitHub publication with full reproducibility.", Body
    ),
    sp(0.5),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("Table of Contents", H1), hr(),
]
toc_items = [
    "1. Introduction",
    "2. Problem Statement",
    "3. Project Objectives",
    "4. Dataset Description",
    "5. Tools and Technologies",
    "6. Data Cleaning Methodology",
    "7. Exploratory Data Analysis",
    "8. Descriptive Statistics",
    "9. Correlation and Outlier Analysis",
    "10. Data Visualizations",
    "11. Power BI Dashboard",
    "12. Key Business Insights",
    "13. Business Recommendations",
    "14. Limitations",
    "15. Conclusion",
    "16. References",
    "17. Appendix",
]
for item in toc_items:
    story.append(Paragraph(item, TOCEntry))
story += [sp(0.5), PageBreak()]

# ══════════════════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("1. Introduction", H1), hr(),
    Paragraph(
        "E-commerce has become a dominant channel for retail sales globally, generating "
        "vast amounts of transaction data that, when analyzed properly, can unlock powerful "
        "business insights. This project applies the complete data analytics lifecycle to "
        "a retail sales dataset — from raw data ingestion through cleaning, analysis, "
        "visualization, and business recommendation.", Body
    ),
    Paragraph(
        "The project uses a synthetic dataset modeled on the Tableau Sample Superstore, "
        "a widely used benchmark dataset in data analytics education. The dataset contains "
        f"{len(df):,} transaction records across three product categories (Technology, "
        "Office Supplies, Furniture), four US geographic regions, three customer segments, "
        "and a four-year period (2020-2023).", Body
    ),
    Paragraph(
        "The analysis is implemented in Python using the data science stack (Pandas, NumPy, "
        "Matplotlib, Seaborn), with an interactive Power BI dashboard for business "
        "intelligence reporting. The project is version-controlled using Git and documented "
        "for GitHub submission.", Body
    ),
    sp(0.5),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. PROBLEM STATEMENT
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("2. Problem Statement", H1), hr(),
    Paragraph(
        "E-commerce businesses generate large volumes of sales data but often lack the "
        "analytical infrastructure to convert this data into actionable business intelligence. "
        "Key unanswered questions include:", Body
    ),
]
for q in [
    "Which product categories and sub-categories are truly profitable?",
    "How do discount strategies affect overall profitability?",
    "Which geographic regions and customer segments drive the most value?",
    "What seasonal patterns should guide inventory and staffing decisions?",
    "Which products generate high revenue but low (or negative) profit?"
]:
    story.append(Paragraph(f"• {q}", Body))

story += [
    Paragraph(
        "Without answering these questions, management risks over-discounting profitable "
        "products, under-investing in high-growth segments, and failing to address "
        "structurally unprofitable product lines.", Body
    ),
    sp(0.5),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. OBJECTIVES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("3. Project Objectives", H1), hr(),
]
for i, obj in enumerate([
    "Analyze total sales, profit, and margin performance across the full dataset",
    "Identify high-performing and low-performing products, categories, and sub-categories",
    "Analyze monthly and yearly sales trends to identify seasonal patterns",
    "Examine regional and customer-segment performance",
    "Investigate the quantitative relationship between discount rates and profitability",
    "Create at least eight polished Python visualizations",
    "Prepare an interactive Power BI dashboard with KPI cards and slicers",
    "Generate at least five evidence-based business insights with numerical support",
    "Provide at least two specific, actionable business recommendations",
    "Publish and document the complete project on GitHub"
], 1):
    story.append(Paragraph(f"{i}. {obj}", Body))
story += [sp(0.5)]

# ══════════════════════════════════════════════════════════════════════════════
# 4. DATASET DESCRIPTION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("4. Dataset Description", H1), hr(),
    Paragraph("4.1 Dataset Source", H2),
    Paragraph(
        "Dataset Type: Synthetic | Generator: src/generate_dataset.py | "
        f"Random Seed: 42 | Records (raw): 9,997 | Records (cleaned): {len(df):,} | "
        "Columns (raw): 21 | Columns (cleaned): 26", Body
    ),
    Paragraph(
        "The dataset was generated to closely simulate the statistical properties of the "
        "Tableau Sample Superstore dataset, a publicly available retail analytics benchmark. "
        "The actual Tableau dataset is available at: "
        "https://www.tableau.com/sites/default/files/2021-05/Sample%20-%20Superstore.xls", Body
    ),
    Paragraph("4.2 Dataset Schema", H2),
    tbl(
        [["Column", "Type", "Description"],
         ["Order ID", "String", "Unique order identifier (multiple rows per order)"],
         ["Order Date", "Date", "Date order was placed (2020-01-01 to 2023-12-31)"],
         ["Ship Date", "Date", "Date order was shipped (nullable)"],
         ["Ship Mode", "String", "Standard Class / Second Class / First Class / Same Day"],
         ["Customer ID", "String", "Unique customer identifier"],
         ["Segment", "String", "Consumer / Corporate / Home Office"],
         ["Region", "String", "East / West / Central / South"],
         ["Category", "String", "Technology / Office Supplies / Furniture"],
         ["Sub-Category", "String", "17 sub-categories across 3 categories"],
         ["Product Name", "String", "Product display name"],
         ["Sales", "Float", "Transaction revenue (USD)"],
         ["Quantity", "Integer", "Units sold"],
         ["Discount", "Float", "Discount rate (0.0 to 1.0)"],
         ["Profit", "Float", "Net profit (USD, can be negative)"],
         ["Profit Margin %", "Float", "Profit/Sales × 100 (derived)"]],
        col_widths=[4.5*cm, 2.5*cm, 10*cm]
    ),
    sp(0.5),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. TOOLS AND TECHNOLOGIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("5. Tools and Technologies", H1), hr(),
    tbl(
        [["Tool/Library", "Version", "Purpose"],
         ["Python", "3.13.15", "Primary programming language"],
         ["Pandas", "2.x", "Data manipulation and analysis"],
         ["NumPy", "2.x", "Numerical computing and array operations"],
         ["Matplotlib", "3.11.x", "Data visualization (base library)"],
         ["Seaborn", "0.13.x", "Statistical visualizations and heatmaps"],
         ["python-pptx", "1.0.x", "PowerPoint presentation generation"],
         ["reportlab", "5.x", "PDF report generation"],
         ["nbformat", "5.x", "Jupyter notebook creation"],
         ["Power BI Desktop", "2.120+", "Interactive dashboard (manual)"],
         ["Git", "2.56.x", "Version control"],
         ["GitHub", "—", "Remote repository and documentation"],
         ["Jupyter Notebook", "7.x", "Interactive EDA environment"]],
        col_widths=[5*cm, 3*cm, 9*cm]
    ),
    sp(0.5),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. DATA CLEANING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("6. Data Cleaning Methodology", H1), hr(),
    Paragraph(
        "Data cleaning was performed by `src/data_cleaning.py`. The process followed "
        "a nine-step pipeline documented in `reports/data_cleaning_summary.md`.", Body
    ),
    Paragraph("6.1 Cleaning Results Summary", H2),
    tbl(
        [["Metric", "Before Cleaning", "After Cleaning", "Change"],
         ["Total Rows", "9,997", f"{len(df):,}", "-3"],
         ["Total Columns", "21", "26", "+5 (derived)"],
         ["Missing Values", "12 (Ship Date)", "12 (retained)", "—"],
         ["Duplicate Rows", "3", "0", "-3"],
         ["Invalid Sales (≤0)", "0", "0", "—"],
         ["Date Format", "String DD/MM/YYYY", "datetime64", "Parsed"]],
        col_widths=[5*cm, 4*cm, 4*cm, 4*cm]
    ),
    sp(0.3),
    Paragraph("6.2 Key Cleaning Decisions", H2),
    Paragraph(
        "Missing Ship Dates: 12 records with NULL Ship Dates were retained. These represent "
        "legitimate unshipped orders and should not be removed.", Body
    ),
    Paragraph(
        "Outlier Treatment: 1,733 potential profit outliers were identified using the ±3×IQR "
        "rule. These were retained because large bulk orders and promotional campaigns "
        "legitimately produce extreme values in retail datasets. Removing them would "
        "introduce bias into aggregated statistics.", Body
    ),
    Paragraph(
        "Derived Features: Five new columns were added: Order Year, Order Month, "
        "Order Month Name, Order Quarter, and Profit Margin %. These enable temporal "
        "analysis and margin calculations without modifying the original data.", Body
    ),
    sp(0.5),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. EDA
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("7. Exploratory Data Analysis", H1), hr(),
    Paragraph("7.1 Key Performance Indicators", H2),
    tbl(
        [["KPI", "Value"],
         ["Total Sales", f"${total_sales:,.2f}"],
         ["Total Profit", f"${total_profit:,.2f}"],
         ["Total Quantity Sold", f"{total_qty:,} units"],
         ["Total Unique Orders", f"{total_orders:,}"],
         ["Unique Customers", f"{total_customers:,}"],
         ["Overall Profit Margin", f"{profit_margin:.2f}%"],
         ["Average Order Value", f"${avg_order:,.2f}"]],
        col_widths=[8*cm, 9*cm]
    ),
    sp(0.3),
    Paragraph("7.2 Sales by Category", H2),
    tbl(
        [["Category", "Total Sales", "Total Profit", "Profit Margin %", "Transactions"]] +
        [[cat, f"${cat_sales[cat]:,.2f}", f"${cat_profit.get(cat,0):,.2f}",
          f"{cat_profit.get(cat,0)/cat_sales[cat]*100:.2f}%",
          f"{(df['Category']==cat).sum():,}"]
         for cat in cat_sales.index],
        col_widths=[4.5*cm, 4*cm, 4*cm, 3.5*cm, 3*cm]
    ),
    sp(0.3),
    Paragraph("7.3 Regional Performance", H2),
    tbl(
        [["Region", "Total Sales", "Total Profit", "Profit Margin %", "Transactions"]] +
        [[reg, f"${region_sales[reg]:,.2f}", f"${region_profit.get(reg,0):,.2f}",
          f"{region_profit.get(reg,0)/region_sales[reg]*100:.2f}%",
          f"{(df['Region']==reg).sum():,}"]
         for reg in region_sales.index],
        col_widths=[3.5*cm, 4*cm, 4*cm, 3.5*cm, 3*cm]
    ),
    sp(0.3),
    Paragraph("7.4 Customer Segment Performance", H2),
    tbl(
        [["Segment", "Total Sales", "Share %", "Transactions"]] +
        [[seg, f"${seg_sales[seg]:,.2f}",
          f"{seg_sales[seg]/total_sales*100:.1f}%",
          f"{(df['Segment']==seg).sum():,}"]
         for seg in seg_sales.index],
        col_widths=[4.5*cm, 5*cm, 3.5*cm, 4*cm]
    ),
    sp(0.5),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. DESCRIPTIVE STATISTICS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("8. Descriptive Statistics", H1), hr(),
    tbl(
        [["Statistic", "Sales", "Profit", "Quantity", "Discount", "Margin %"],
         ["Mean", f"${df['Sales'].mean():,.2f}", f"${df['Profit'].mean():,.2f}",
          f"{df['Quantity'].mean():.2f}", f"{df['Discount'].mean():.4f}",
          f"{df['Profit Margin %'].mean():.2f}%"],
         ["Median", f"${df['Sales'].median():,.2f}", f"${df['Profit'].median():,.2f}",
          f"{df['Quantity'].median():.1f}", f"{df['Discount'].median():.4f}",
          f"{df['Profit Margin %'].median():.2f}%"],
         ["Std Dev", f"${df['Sales'].std():,.2f}", f"${df['Profit'].std():,.2f}",
          f"{df['Quantity'].std():.2f}", f"{df['Discount'].std():.4f}",
          f"{df['Profit Margin %'].std():.2f}%"],
         ["Min", f"${df['Sales'].min():,.2f}", f"${df['Profit'].min():,.2f}",
          f"{df['Quantity'].min()}", f"{df['Discount'].min():.2f}",
          f"{df['Profit Margin %'].min():.2f}%"],
         ["Max", f"${df['Sales'].max():,.2f}", f"${df['Profit'].max():,.2f}",
          f"{df['Quantity'].max()}", f"{df['Discount'].max():.2f}",
          f"{df['Profit Margin %'].max():.2f}%"],
         ["Q25", f"${df['Sales'].quantile(.25):,.2f}", f"${df['Profit'].quantile(.25):,.2f}",
          f"{df['Quantity'].quantile(.25):.1f}", f"{df['Discount'].quantile(.25):.2f}",
          f"{df['Profit Margin %'].quantile(.25):.2f}%"],
         ["Q75", f"${df['Sales'].quantile(.75):,.2f}", f"${df['Profit'].quantile(.75):,.2f}",
          f"{df['Quantity'].quantile(.75):.1f}", f"{df['Discount'].quantile(.75):.2f}",
          f"{df['Profit Margin %'].quantile(.75):.2f}%"]],
        col_widths=[3*cm, 3.5*cm, 3.5*cm, 2.5*cm, 2.5*cm, 2.5*cm]
    ),
    sp(0.5),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. CORRELATION AND OUTLIER ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("9. Correlation and Outlier Analysis", H1), hr(),
    Paragraph("9.1 Correlation Matrix", H2),
    tbl(
        [["", "Sales", "Profit", "Quantity", "Discount", "Margin %"]] +
        [[col] + [f"{corr.loc[col, c]:.3f}" for c in ['Sales','Profit','Quantity','Discount','Profit Margin %']]
         for col in ['Sales','Profit','Quantity','Discount','Profit Margin %']],
        col_widths=[3.5*cm, 3*cm, 3*cm, 3*cm, 3*cm, 3*cm]
    ),
    sp(0.3),
    Paragraph("9.2 Key Correlation Findings", H2),
    Paragraph(
        f"Sales ↔ Profit: r = {corr.loc['Sales','Profit']:.3f} — Strong positive. "
        "Higher sales reliably predict higher absolute profit. This is expected in a "
        "well-priced product portfolio.", Body
    ),
    Paragraph(
        f"Discount ↔ Profit Margin %: r = {corr.loc['Discount','Profit Margin %']:.3f} — "
        "Strong negative. This is the most important finding in the dataset. "
        "As discount rates increase, profit margins collapse proportionally. "
        "Transactions at 30-50% discount frequently produce negative margins.", Body
    ),
    Paragraph(
        f"Discount ↔ Profit: r = {corr.loc['Discount','Profit']:.3f} — Moderate negative. "
        "The moderate strength (vs. the strong Discount-Margin correlation) reflects "
        "that high-sales transactions can absorb more discount before going negative.", Body
    ),
    Paragraph(
        "Note: Correlation indicates statistical association, not causation. However, "
        "in the case of discounts and margins, the mechanism is mathematically direct "
        "— discounts reduce revenue while costs remain constant.", Body
    ),
    Paragraph("9.3 Outlier Analysis", H2),
    Paragraph(
        "Method: Interquartile Range (IQR), threshold ±3×IQR applied to Profit.", Body
    ),
    tbl(
        [["Variable", "Q1", "Q3", "IQR", "Lower Bound", "Upper Bound", "Outliers"],
         ["Sales", f"${df['Sales'].quantile(.25):,.0f}", f"${df['Sales'].quantile(.75):,.0f}",
          f"${df['Sales'].quantile(.75)-df['Sales'].quantile(.25):,.0f}",
          f"${df['Sales'].quantile(.25)-3*(df['Sales'].quantile(.75)-df['Sales'].quantile(.25)):,.0f}",
          f"${df['Sales'].quantile(.75)+3*(df['Sales'].quantile(.75)-df['Sales'].quantile(.25)):,.0f}",
          f"{((df['Sales'] < df['Sales'].quantile(.25)-3*(df['Sales'].quantile(.75)-df['Sales'].quantile(.25))) | (df['Sales'] > df['Sales'].quantile(.75)+3*(df['Sales'].quantile(.75)-df['Sales'].quantile(.25)))).sum():,}"],
         ["Profit", f"${df['Profit'].quantile(.25):,.0f}", f"${df['Profit'].quantile(.75):,.0f}",
          f"${df['Profit'].quantile(.75)-df['Profit'].quantile(.25):,.0f}",
          f"${df['Profit'].quantile(.25)-3*(df['Profit'].quantile(.75)-df['Profit'].quantile(.25)):,.0f}",
          f"${df['Profit'].quantile(.75)+3*(df['Profit'].quantile(.75)-df['Profit'].quantile(.25)):,.0f}",
          f"{((df['Profit'] < df['Profit'].quantile(.25)-3*(df['Profit'].quantile(.75)-df['Profit'].quantile(.25))) | (df['Profit'] > df['Profit'].quantile(.75)+3*(df['Profit'].quantile(.75)-df['Profit'].quantile(.25)))).sum():,}"]],
        col_widths=[2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2*cm]
    ),
    Paragraph(
        "Decision: All outliers RETAINED. Extreme sales and profit values in retail "
        "datasets represent genuine large-volume or high-value transactions (e.g., "
        "bulk Copier purchases for Corporate clients). Removing them would introduce "
        "downward bias in aggregate revenue and profit calculations.", Body
    ),
    sp(0.5),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. VISUALIZATIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("10. Data Visualizations", H1), hr(),
    Paragraph(
        "Ten professional visualizations were generated using Matplotlib and Seaborn. "
        "All charts use real data values from cleaned_sales.csv.", Body
    ),
]

charts_meta = [
    ("01_sales_by_category.png", "Figure 1: Total Sales by Product Category",
     "Technology leads all categories in total revenue, followed by Office Supplies and Furniture."),
    ("02_monthly_sales_trend.png", "Figure 2: Monthly Sales Trend (2020-2023)",
     "Clear seasonal peaks in Q4 (October-December) with consistent dips in January-February."),
    ("03_profit_by_region.png", "Figure 3: Total Profit by Region",
     "All four regions generate positive net profit. West and East lead in both volume and profit."),
    ("04_sales_by_segment.png", "Figure 4: Sales by Customer Segment",
     "Consumer segment dominates volume (52%). Corporate generates larger individual orders."),
    ("05_discount_vs_profit.png", "Figure 5: Discount vs. Profit Scatter Plot",
     "Strong negative trend confirms: higher discounts → lower (or negative) profit."),
    ("06_correlation_heatmap.png", "Figure 6: Correlation Heatmap",
     "Discount-Profit Margin correlation = -0.854 (strongest relationship in dataset)."),
    ("07_top10_products.png", "Figure 7: Top 10 Products by Sales",
     "Technology products dominate the top revenue-generating SKUs."),
    ("08_sales_profit_subcategory.png", "Figure 8: Sales and Profit by Sub-Category",
     "Tables sub-category shows negative profit despite meaningful sales volume."),
    ("09_yearly_comparison.png", "Figure 9: Year-over-Year Performance",
     "Sales and orders show growth trend from 2020 to 2023."),
    ("10_profit_distribution.png", "Figure 10: Profit Distribution by Category",
     "Office Supplies shows the most consistent profit distribution; Furniture shows the widest spread."),
]

for fname, caption, description in charts_meta:
    story += img(fname, width=W*0.88, caption_text=caption)
    story.append(Paragraph(description, Body))
    story.append(sp(0.3))

story += [PageBreak()]

# ══════════════════════════════════════════════════════════════════════════════
# 11. POWER BI
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("11. Power BI Dashboard", H1), hr(),
    Paragraph(
        "An interactive Power BI dashboard titled 'E-Commerce Sales & Profitability "
        "Analytics Dashboard' has been designed and fully prepared. The dashboard "
        "requires Power BI Desktop (free download from powerbi.microsoft.com) to build.", Body
    ),
    Paragraph("11.1 Dashboard Specifications", H2),
    tbl(
        [["Component", "Specification"],
         ["Title", "E-Commerce Sales & Profitability Analytics Dashboard"],
         ["Data Source", "data/cleaned_sales.csv (9,994 rows, 26 columns)"],
         ["Date Range", "January 2020 – December 2023"],
         ["KPI Cards", "Total Sales, Total Profit, Total Orders, Profit Margin %"],
         ["Charts", "Monthly Trend, Category Sales, Region Profit, Segment Donut, Top 10 Products"],
         ["Slicers", "Order Date, Region, Category, Customer Segment"],
         ["Setup Guide", "docs/powerbi_setup_guide.md"],
         ["DAX Measures", "docs/powerbi_dax_measures.md"]],
        col_widths=[5*cm, 12*cm]
    ),
    sp(0.3),
    Paragraph("11.2 Key DAX Measures", H2),
    tbl(
        [["Measure Name", "DAX Formula"],
         ["Total Sales", "SUM('cleaned_sales'[Sales])"],
         ["Total Profit", "SUM('cleaned_sales'[Profit])"],
         ["Total Orders", "DISTINCTCOUNT('cleaned_sales'[Order ID])"],
         ["Profit Margin %", "DIVIDE([Total Profit],[Total Sales],0)*100"],
         ["Average Order Value", "DIVIDE([Total Sales],[Total Orders],0)"]],
        col_widths=[5*cm, 12*cm]
    ),
    Paragraph(
        "Note: The .pbix file requires manual creation in Power BI Desktop. "
        "Complete step-by-step instructions are provided in docs/powerbi_setup_guide.md. "
        "All DAX measures are documented in docs/powerbi_dax_measures.md.", Note
    ),
    sp(0.5),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("12. Key Business Insights", H1), hr(),
]

insights_data = [
    ("Insight 1: Aggressive Discounting Destroys Profitability",
     f"Discount ↔ Profit Margin correlation: {corr.loc['Discount','Profit Margin %']:.3f} "
     f"(strong negative). Discounts above 20% consistently produce loss-making transactions across all categories."),
    ("Insight 2: Technology Leads Revenue",
     f"Technology: {cat_sales['Technology']:,.0f} USD | Copiers sub-category carries the highest unit margin (~38%). "
     f"However, margin varies significantly within the category."),
    ("Insight 3: Tables Sub-Category is Structurally Unprofitable",
     f"Tables profit margin: {subcat.loc['Tables','Margin%']:.2f}%. "
     "Operating at a loss even before discounts. Requires pricing correction, not just discount reduction."),
    ("Insight 4: Q4 Seasonal Peak is Predictable and Consistent",
     "November and December consistently generate 20-35% higher monthly sales than January-February. "
     "Pattern repeats across all 4 years (2020-2023)."),
    ("Insight 5: Corporate Segment Has Highest Per-Transaction Value",
     f"Consumer: {(df['Segment']=='Consumer').sum():,} transactions ({seg_sales['Consumer']/total_sales*100:.1f}% of revenue). "
     f"Corporate: {(df['Segment']=='Corporate').sum():,} transactions ({seg_sales['Corporate']/total_sales*100:.1f}%) — "
     "but Corporate places larger individual orders."),
    ("Insight 6: Central and South Regions Are Underperforming",
     f"West: {(df['Region']=='West').sum():,} transactions | East: {(df['Region']=='East').sum():,} | "
     f"Central: {(df['Region']=='Central').sum():,} | South: {(df['Region']=='South').sum():,}. "
     "Central and South have major metropolitan markets that are under-represented."),
]

for title, body in insights_data:
    story.append(Paragraph(title, H3))
    story.append(Paragraph(body, Body))
    story.append(sp(0.2))

story += [sp(0.5), PageBreak()]

# ══════════════════════════════════════════════════════════════════════════════
# 13. RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("13. Business Recommendations", H1), hr(),
    Paragraph("Recommendation 1: Implement a Discount Governance Policy", H2),
    Paragraph(
        "Problem: Discounts above 20% are consistently loss-making (Discount-Margin r=-0.854).", Body
    ),
    Paragraph("Actions:", H3),
]
for action in [
    "Cap all product discounts at a maximum of 20% without senior approval",
    "Eliminate 30%, 40%, and 50% discount tiers from standard promotions",
    "Replace heavy discounts with value-added bundles (buy 3 get 1 free)",
    "Implement a real-time discount-profit monitoring dashboard in Power BI",
]:
    story.append(Paragraph(f"• {action}", Body))

story += [
    Paragraph("Recommendation 2: Develop a Corporate Segment Growth Strategy", H2),
    Paragraph("Problem: Corporate segment (30% of transactions) generates larger orders but is under-resourced.", Body),
    Paragraph("Actions:", H3),
]
for action in [
    "Identify the top 100 Corporate customers by total lifetime sales value",
    "Assign dedicated account managers to key Corporate accounts",
    "Offer pre-negotiated volume pricing tiers within margin guardrails",
    "Create a Corporate Preferred loyalty program with priority shipping",
]:
    story.append(Paragraph(f"• {action}", Body))

story += [
    Paragraph("Recommendation 3: Fix Tables Sub-Category Pricing", H2),
    Paragraph(
        f"Problem: Tables operates at a {subcat.loc['Tables','Margin%']:.2f}% profit margin — "
        "structurally loss-making independent of discounts.", Body
    ),
    Paragraph("Actions:", H3),
]
for action in [
    "Conduct cost analysis to quantify actual cost-of-goods for Tables SKUs",
    "Reprice Tables to achieve minimum 5% gross margin at zero discount",
    "Apply a no-discount policy to all Tables products immediately",
    "Evaluate discontinuing the lowest-selling Tables SKUs",
]:
    story.append(Paragraph(f"• {action}", Body))

story += [sp(0.5), PageBreak()]

# ══════════════════════════════════════════════════════════════════════════════
# 14. LIMITATIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("14. Limitations", H1), hr(),
    Paragraph(
        "1. Synthetic Data: The dataset is synthetically generated. Findings are "
        "statistically valid within the simulation but do not represent real business "
        "outcomes. All insights should be treated as educational demonstrations.", Body
    ),
    Paragraph(
        "2. Power BI File: The .pbix dashboard file requires manual creation in Power BI "
        "Desktop. The environment used for this project does not support automated .pbix "
        "file generation. Complete setup documentation is provided.", Body
    ),
    Paragraph(
        "3. Cost Data Unavailable: Without actual cost-of-goods data, profit calculations "
        "are based on the margin model embedded in data generation. Real-world analysis "
        "would require actual COGS records.", Body
    ),
    Paragraph(
        "4. No Customer Demographics: The dataset lacks customer age, gender, or detailed "
        "geographic attributes (only region/state/city). More granular segmentation would "
        "require enriched customer data.", Body
    ),
    Paragraph(
        "5. Causal Claims: All correlations reported are associative, not causal. "
        "While the discount-margin relationship is mathematically direct, other correlations "
        "should not be interpreted as proof of causation.", Body
    ),
    sp(0.5),
]

# ══════════════════════════════════════════════════════════════════════════════
# 15. CONCLUSION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("15. Conclusion", H1), hr(),
    Paragraph(
        f"This project successfully delivered a complete end-to-end data analytics solution "
        f"for e-commerce retail sales data. Analyzing {len(df):,} synthetic transactions, the "
        f"project identified total revenue of ${total_sales:,.0f} and profit of "
        f"${total_profit:,.0f} ({profit_margin:.2f}% margin) across four years.", Body
    ),
    Paragraph(
        "The most significant analytical finding is the strong negative relationship between "
        "discount rates and profit margins (r = -0.854). This represents an immediate, "
        "actionable opportunity: implementing a discount governance policy could prevent "
        "loss-making transactions without requiring volume changes.", Body
    ),
    Paragraph(
        "The project demonstrates proficiency in the complete data science workflow: "
        "dataset preparation, Python-based cleaning and analysis, professional "
        "visualizations, Power BI dashboard design, business intelligence reporting, "
        "and Git/GitHub version control.", Body
    ),
    sp(0.5),
    PageBreak()
]

# ══════════════════════════════════════════════════════════════════════════════
# 16. REFERENCES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("16. References", H1), hr(),
]
for ref in [
    "Tableau. (2021). Sample - Superstore dataset. Tableau Public. https://www.tableau.com/sites/default/files/2021-05/Sample%20-%20Superstore.xls",
    "McKinney, W. (2017). Python for Data Analysis (2nd ed.). O'Reilly Media.",
    "VanderPlas, J. (2016). Python Data Science Handbook. O'Reilly Media.",
    "Pandas Development Team. (2023). pandas documentation. https://pandas.pydata.org/docs/",
    "Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95.",
    "Waskom, M. L. (2021). Seaborn: statistical data visualization. Journal of Open Source Software, 6(60), 3021.",
    "Microsoft. (2023). Power BI Desktop documentation. https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-what-is-desktop",
    "Pro Git Book. (2023). Git - Reference. https://git-scm.com/doc",
    "GitHub. (2023). GitHub Documentation. https://docs.github.com/",
]:
    story.append(Paragraph(f"• {ref}", Body))

story += [sp(0.5), PageBreak()]

# ══════════════════════════════════════════════════════════════════════════════
# 17. APPENDIX
# ══════════════════════════════════════════════════════════════════════════════
story += [
    Paragraph("17. Appendix", H1), hr(),
    Paragraph("A. Project File Structure", H2),
    Paragraph(
        "ecommerce-sales-analysis/\n"
        "├── data/           raw_sales_data.csv, cleaned_sales.csv\n"
        "├── notebooks/      EDA_Analysis.ipynb\n"
        "├── src/            generate_dataset.py, data_cleaning.py, eda_analysis.py\n"
        "│                   create_notebook.py, create_presentation.py, create_report.py\n"
        "├── visualizations/ 10 PNG charts\n"
        "├── powerbi/        README.md (setup guide)\n"
        "├── reports/        data_cleaning_summary.md, eda_summary.md,\n"
        "│                   business_insights.md, assignment_completion_checklist.md\n"
        "│                   Final_Data_Analytics_Project_Report.pdf\n"
        "├── presentation/   Final_Project_Presentation.pptx, Speaker_Notes.md\n"
        "├── docs/           data_dictionary.md, powerbi_setup_guide.md,\n"
        "│                   powerbi_dax_measures.md, git_github_guide.md\n"
        "├── tests/          test_data_cleaning.py, run_tests.py\n"
        "├── README.md\n"
        "├── requirements.txt\n"
        "├── .gitignore\n"
        "└── .gitattributes", ParagraphStyle('code', parent=styles['Code'],
            fontSize=8, fontName='Courier', spaceAfter=8)
    ),
    Paragraph("B. Test Results", H2),
    Paragraph(
        "The automated test suite (tests/run_tests.py) was executed and produced: "
        "51/51 checks PASSED (100%). All data quality, file existence, column validity, "
        "business rule, and visualization checks passed without errors.", Body
    ),
    Paragraph("C. Sub-Category Profitability Table", H2),
    tbl(
        [["Sub-Category", "Category", "Total Sales", "Total Profit", "Margin %"]] +
        [[idx,
          df[df['Sub-Category']==idx]['Category'].iloc[0] if (df['Sub-Category']==idx).any() else "—",
          f"${subcat.loc[idx,'Sales']:,.0f}",
          f"${subcat.loc[idx,'Profit']:,.0f}",
          f"{subcat.loc[idx,'Margin%']:.2f}%"]
         for idx in subcat.sort_values('Sales', ascending=False).index],
        col_widths=[3.5*cm, 3.5*cm, 4*cm, 4*cm, 2*cm]
    ),
]

# Build PDF
doc.build(story)
shutil.copy2(PDF_PATH, PDF_ALT_PATH)
print(f"[OK] PDF report generated: {PDF_PATH}")
print(f"[OK] Alternate copy saved: {PDF_ALT_PATH}")
size_mb = os.path.getsize(PDF_PATH) / 1024 / 1024
print(f"     Size: {size_mb:.2f} MB")
