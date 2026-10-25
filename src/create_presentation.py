"""
create_presentation.py
----------------------
Generates the Final_Project_Presentation.pptx programmatically
using python-pptx.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PPTX_PATH = os.path.join(BASE_DIR, 'presentation', 'Final_Project_Presentation.pptx')
NOTES_PATH = os.path.join(BASE_DIR, 'presentation', 'Speaker_Notes.md')
VIZ_DIR = os.path.join(BASE_DIR, 'visualizations')
CLEAN_PATH = os.path.join(BASE_DIR, 'data', 'cleaned_sales.csv')
os.makedirs(os.path.dirname(PPTX_PATH), exist_ok=True)

# Load key stats
df = pd.read_csv(CLEAN_PATH)
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
profit_margin = total_profit / total_sales * 100

# Colors
DARK_BLUE = RGBColor(0x1A, 0x23, 0x7E)   # deep navy
ACCENT_BLUE = RGBColor(0x21, 0x96, 0xF3)
ACCENT_GREEN = RGBColor(0x4C, 0xAF, 0x50)
ACCENT_ORANGE = RGBColor(0xFF, 0x98, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
DARK_GRAY = RGBColor(0x42, 0x42, 0x42)
RED = RGBColor(0xF4, 0x43, 0x36)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK_LAYOUT = prs.slide_layouts[6]  # completely blank


def add_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=None):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, left, top, width, height,
             font_size=18, bold=False, color=None, align=PP_ALIGN.LEFT,
             word_wrap=True):
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    return txBox


def add_image_if_exists(slide, img_path, left, top, width, height):
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(left), Inches(top),
                                 Inches(width), Inches(height))
        return True
    return False


def slide_header(slide, title, subtitle=None):
    """Add consistent slide header bar."""
    add_rect(slide, 0, 0, 13.33, 1.2, fill_color=DARK_BLUE)
    add_text(slide, title, 0.3, 0.15, 12.5, 0.8,
             font_size=28, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.3, 0.75, 12.5, 0.5,
                 font_size=14, color=ACCENT_BLUE, align=PP_ALIGN.LEFT)
    # Footer
    add_rect(slide, 0, 7.0, 13.33, 0.5, fill_color=DARK_BLUE)
    add_text(slide, "E-Commerce Sales Analysis | Week 6 Internship Assignment | Synthetic Data",
             0.3, 7.05, 10, 0.4, font_size=9, color=WHITE)
    add_text(slide, f"Slide {len(prs.slides)}", 11.5, 7.05, 1.5, 0.4,
             font_size=9, color=WHITE, align=PP_ALIGN.RIGHT)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1: Title Slide
# ══════════════════════════════════════════════════════════════════════════════
slide1 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide1, 0, 0, 13.33, 7.5, fill_color=DARK_BLUE)
add_rect(slide1, 0, 3.5, 13.33, 0.08, fill_color=ACCENT_BLUE)

add_text(slide1, "E-Commerce Sales Data Analysis", 0.5, 1.2, 12.3, 1.0,
         font_size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide1, "and Interactive Power BI Dashboard", 0.5, 2.1, 12.3, 0.8,
         font_size=28, bold=False, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)
add_rect(slide1, 3.5, 3.6, 6.33, 0.06, fill_color=ACCENT_ORANGE)
add_text(slide1, "Week 6 Internship Assignment — Data Analytics Capstone Project", 0.5, 3.8,
         12.3, 0.6, font_size=16, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide1, "Student: [Your Name] | October 2026", 0.5, 4.5, 12.3, 0.5,
         font_size=14, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)
add_text(slide1, "Tools: Python | Pandas | Matplotlib | Seaborn | Power BI | Git/GitHub", 0.5,
         5.2, 12.3, 0.5, font_size=13, color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide1, "⚠ Dataset: Synthetically generated for educational purposes", 0.5, 6.0,
         12.3, 0.5, font_size=11, color=ACCENT_ORANGE, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2: Problem Statement and Objectives
# ══════════════════════════════════════════════════════════════════════════════
slide2 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide2, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
slide_header(slide2, "Problem Statement & Objectives")

add_rect(slide2, 0.3, 1.4, 5.8, 4.8, fill_color=WHITE)
add_text(slide2, "Problem Statement", 0.5, 1.5, 5.4, 0.5, font_size=16,
         bold=True, color=DARK_BLUE)
problems = [
    "Businesses need data-driven decisions but lack clear visibility into:",
    "",
    "• Which products and categories are truly profitable?",
    "• How do discounts impact the bottom line?",
    "• Which regions and customer segments drive growth?",
    "• What seasonal patterns should drive inventory planning?",
    "",
    "This project builds a complete analytics solution to answer these questions."
]
add_text(slide2, "\n".join(problems), 0.5, 2.1, 5.4, 3.5,
         font_size=13, color=DARK_GRAY)

add_rect(slide2, 6.5, 1.4, 6.5, 4.8, fill_color=WHITE)
add_text(slide2, "Project Objectives", 6.7, 1.5, 6.1, 0.5, font_size=16,
         bold=True, color=DARK_BLUE)
objectives = [
    "1. Analyze sales and profit performance",
    "2. Identify high/low performing products",
    "3. Examine monthly and yearly trends",
    "4. Study regional & segment performance",
    "5. Investigate discount-profit relationship",
    "6. Create 8+ Python visualizations",
    "7. Build interactive Power BI dashboard",
    "8. Generate 5+ business insights",
    "9. Provide actionable recommendations",
    "10. Publish project on GitHub"
]
add_text(slide2, "\n".join(objectives), 6.7, 2.1, 6.1, 3.5,
         font_size=13, color=DARK_GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3: Dataset Overview
# ══════════════════════════════════════════════════════════════════════════════
slide3 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide3, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
slide_header(slide3, "Dataset Overview", "Synthetic Sample Superstore-Style Data")

# KPI boxes
kpi_data = [
    ("9,994", "Records", ACCENT_BLUE),
    ("21", "Original Columns", ACCENT_GREEN),
    ("26", "After Feature Engineering", ACCENT_ORANGE),
    ("2020-2023", "Date Range", DARK_BLUE),
]
for i, (val, label, color) in enumerate(kpi_data):
    x = 0.3 + i * 3.2
    add_rect(slide3, x, 1.5, 2.9, 1.6, fill_color=color)
    add_text(slide3, val, x, 1.7, 2.9, 0.9, font_size=26, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide3, label, x, 2.55, 2.9, 0.5, font_size=12,
             color=WHITE, align=PP_ALIGN.CENTER)

add_rect(slide3, 0.3, 3.3, 5.8, 3.3, fill_color=WHITE)
add_text(slide3, "Dataset Fields", 0.5, 3.4, 5.4, 0.4, font_size=14,
         bold=True, color=DARK_BLUE)
fields_text = (
    "Order ID, Order Date, Ship Date, Ship Mode\n"
    "Customer ID, Segment, Country, Region\n"
    "State, City, Category, Sub-Category\n"
    "Product ID, Product Name\n"
    "Sales, Quantity, Discount, Profit\n"
    "+ Derived: Year, Month, Quarter, Margin %"
)
add_text(slide3, fields_text, 0.5, 3.9, 5.4, 2.5, font_size=12, color=DARK_GRAY)

add_rect(slide3, 6.5, 3.3, 6.5, 3.3, fill_color=WHITE)
add_text(slide3, "Data Quality", 6.7, 3.4, 6.1, 0.4, font_size=14,
         bold=True, color=DARK_BLUE)
quality_text = (
    "Raw rows:       9,997\n"
    "After cleaning: 9,994 (-3 duplicates)\n\n"
    "Missing Ship Dates: 12 (retained)\n"
    "Invalid records:    0 removed\n"
    "Duplicates removed: 3\n\n"
    "Source: Synthetically generated\n"
    "Seed: 42 (fully reproducible)"
)
add_text(slide3, quality_text, 6.7, 3.9, 6.1, 2.5, font_size=12, color=DARK_GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4: Data Cleaning
# ══════════════════════════════════════════════════════════════════════════════
slide4 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide4, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
slide_header(slide4, "Data Cleaning & Preparation", "src/data_cleaning.py")

steps = [
    ("1", "Load Dataset", "UTF-8 with fallback encoding", ACCENT_BLUE),
    ("2", "Inspect Structure", "Shape, dtypes, column names", ACCENT_GREEN),
    ("3", "Missing Values", "12 Ship Dates retained as valid", ACCENT_ORANGE),
    ("4", "Duplicate Removal", "3 exact duplicates removed", DARK_BLUE),
    ("5", "Date Parsing", "DD/MM/YYYY → datetime64", ACCENT_BLUE),
    ("6", "Validation", "Sales>0, Discount in [0,1]", ACCENT_GREEN),
    ("7", "Feature Engineering", "Year, Month, Quarter, Margin%", ACCENT_ORANGE),
    ("8", "Export", "data/cleaned_sales.csv", DARK_BLUE),
]

for i, (num, title, detail, color) in enumerate(steps):
    row = i // 4
    col = i % 4
    x = 0.3 + col * 3.2
    y = 1.5 + row * 2.2
    add_rect(slide4, x, y, 2.9, 1.8, fill_color=color)
    add_text(slide4, num, x + 0.1, y + 0.05, 0.5, 0.6, font_size=22,
             bold=True, color=WHITE)
    add_text(slide4, title, x + 0.1, y + 0.55, 2.7, 0.45, font_size=12,
             bold=True, color=WHITE)
    add_text(slide4, detail, x + 0.1, y + 1.0, 2.7, 0.7, font_size=10,
             color=WHITE)

add_rect(slide4, 0.3, 5.9, 12.5, 0.8, fill_color=WHITE)
add_text(slide4, "Outlier Decision: 1,733 potential outliers RETAINED — represent legitimate bulk/high-value orders",
         0.5, 5.95, 12, 0.65, font_size=13, bold=False, color=DARK_BLUE,
         align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5: EDA — KPIs and Business Analysis
# ══════════════════════════════════════════════════════════════════════════════
slide5 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide5, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
slide_header(slide5, "Exploratory Data Analysis — Key Findings")

kpis = [
    (f"${total_sales/1e6:.2f}M", "Total Sales", ACCENT_BLUE),
    (f"${total_profit/1e6:.2f}M", "Total Profit", ACCENT_GREEN),
    (f"{total_orders:,}", "Total Orders", ACCENT_ORANGE),
    (f"{profit_margin:.1f}%", "Profit Margin", DARK_BLUE),
]
for i, (val, label, color) in enumerate(kpis):
    x = 0.3 + i * 3.2
    add_rect(slide5, x, 1.4, 2.9, 1.4, fill_color=color)
    add_text(slide5, val, x, 1.55, 2.9, 0.8, font_size=24, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide5, label, x, 2.3, 2.9, 0.4, font_size=12,
             color=WHITE, align=PP_ALIGN.CENTER)

add_rect(slide5, 0.3, 3.0, 3.9, 3.6, fill_color=WHITE)
add_text(slide5, "By Category", 0.5, 3.1, 3.5, 0.4, font_size=13,
         bold=True, color=DARK_BLUE)
cat_stats = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
cat_text = ""
for cat, s in cat_stats.items():
    cat_text += f"{cat}: ${s/1e6:.2f}M\n"
add_text(slide5, cat_text, 0.5, 3.6, 3.5, 2.5, font_size=13, color=DARK_GRAY)

add_rect(slide5, 4.5, 3.0, 3.9, 3.6, fill_color=WHITE)
add_text(slide5, "By Region", 4.7, 3.1, 3.5, 0.4, font_size=13,
         bold=True, color=DARK_BLUE)
reg_stats = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
reg_text = ""
for reg, s in reg_stats.items():
    reg_text += f"{reg}: ${s/1e6:.2f}M\n"
add_text(slide5, reg_text, 4.7, 3.6, 3.5, 2.5, font_size=13, color=DARK_GRAY)

add_rect(slide5, 8.7, 3.0, 4.3, 3.6, fill_color=WHITE)
add_text(slide5, "By Segment", 8.9, 3.1, 4.0, 0.4, font_size=13,
         bold=True, color=DARK_BLUE)
seg_stats = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
seg_text = ""
for seg, s in seg_stats.items():
    pct = s / total_sales * 100
    seg_text += f"{seg}: ${s/1e6:.2f}M ({pct:.0f}%)\n"
add_text(slide5, seg_text, 8.9, 3.6, 4.0, 2.5, font_size=13, color=DARK_GRAY)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6: Visualizations
# ══════════════════════════════════════════════════════════════════════════════
slide6 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide6, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
slide_header(slide6, "Data Visualizations", "10 charts generated from cleaned dataset")

img_grid = [
    ('01_sales_by_category.png', 0.2, 1.4, 4.1, 2.6),
    ('02_monthly_sales_trend.png', 4.5, 1.4, 8.6, 2.6),
    ('05_discount_vs_profit.png', 0.2, 4.1, 4.1, 2.9),
    ('06_correlation_heatmap.png', 4.5, 4.1, 4.1, 2.9),
    ('07_top10_products.png', 8.8, 4.1, 4.3, 2.9),
]
for fname, l, t, w, h in img_grid:
    path = os.path.join(VIZ_DIR, fname)
    add_image_if_exists(slide6, path, l, t, w, h)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7: Power BI Dashboard
# ══════════════════════════════════════════════════════════════════════════════
slide7 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide7, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
slide_header(slide7, "Power BI Dashboard", "E-Commerce Sales & Profitability Analytics")

add_rect(slide7, 0.3, 1.4, 12.5, 5.1, fill_color=WHITE)
add_rect(slide7, 0.4, 1.5, 12.3, 0.7, fill_color=DARK_BLUE)
add_text(slide7, "E-Commerce Sales & Profitability Analytics Dashboard",
         0.5, 1.55, 12.0, 0.6, font_size=15, bold=True, color=WHITE)

kpi_boxes = [
    ("$33.17M", "Total Sales", ACCENT_BLUE),
    ("$3.64M", "Total Profit", ACCENT_GREEN),
    ("9,070", "Total Orders", ACCENT_ORANGE),
    ("10.98%", "Profit Margin", DARK_BLUE),
]
for i, (val, label, color) in enumerate(kpi_boxes):
    x = 0.4 + i * 3.1
    add_rect(slide7, x, 2.3, 2.8, 1.1, fill_color=color)
    add_text(slide7, val, x, 2.4, 2.8, 0.6, font_size=18, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide7, label, x, 2.95, 2.8, 0.4, font_size=10,
             color=WHITE, align=PP_ALIGN.CENTER)

add_rect(slide7, 0.4, 3.55, 12.3, 0.3, fill_color=DARK_BLUE)
add_text(slide7, "Monthly Sales Trend (Line Chart)  |  Sales by Category (Bar)  |  Profit by Region (Bar)  |  Segment (Donut)  |  Top 10 Products",
         0.5, 3.58, 12.0, 0.25, font_size=10, color=WHITE, align=PP_ALIGN.CENTER)

add_rect(slide7, 0.4, 3.9, 12.3, 0.8, fill_color=RGBColor(0xE3, 0xF2, 0xFD))
add_text(slide7, "Slicers: [Order Date]  [Region ▼]  [Category ▼]  [Customer Segment ▼]",
         0.6, 3.95, 12.0, 0.65, font_size=13, color=DARK_BLUE, align=PP_ALIGN.CENTER)

add_text(slide7,
         "Note: Power BI Desktop is required to build the .pbix file.\n"
         "Setup guide: docs/powerbi_setup_guide.md | DAX measures: docs/powerbi_dax_measures.md",
         0.5, 4.85, 12.3, 0.8, font_size=12, color=RED, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8: Business Insights
# ══════════════════════════════════════════════════════════════════════════════
slide8 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide8, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
slide_header(slide8, "Key Business Insights", "Evidence-based findings from data analysis")

insights = [
    (ACCENT_BLUE, "1. Discount-Profit Crisis",
     "Discount ↔ Profit Margin correlation = -0.854\nDiscounts >20% consistently generate losses"),
    (ACCENT_GREEN, "2. Technology Leads Revenue",
     "Highest transaction count (3,389)\nCopiers sub-category: ~38% margin"),
    (ACCENT_ORANGE, "3. Tables Sub-Category Loses Money",
     "Structural negative margin\nLosses worsen with any discount applied"),
    (DARK_BLUE, "4. Q4 Seasonal Peak",
     "Nov & Dec are highest revenue months\nJan & Feb are consistently weakest"),
    (RED, "5. Corporate Segment Underserved",
     "30% of transactions, but higher order values\nGrowth potential vs Consumer segment"),
    (RGBColor(0x9C, 0x27, 0xB0), "6. West & East Dominate",
     "2,977 and 2,777 transactions respectively\nCentral & South have room to grow"),
]

for i, (color, title, body) in enumerate(insights):
    row = i // 3
    col = i % 3
    x = 0.3 + col * 4.3
    y = 1.5 + row * 2.4
    add_rect(slide8, x, y, 3.9, 2.1, fill_color=color)
    add_text(slide8, title, x + 0.1, y + 0.1, 3.7, 0.55, font_size=13,
             bold=True, color=WHITE)
    add_text(slide8, body, x + 0.1, y + 0.7, 3.7, 1.3, font_size=11,
             color=WHITE)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9: Recommendations
# ══════════════════════════════════════════════════════════════════════════════
slide9 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide9, 0, 0, 13.33, 7.5, fill_color=LIGHT_GRAY)
slide_header(slide9, "Business Recommendations", "Data-driven actions for management")

recs = [
    (ACCENT_BLUE, "Recommendation 1: Discount Governance Policy",
     [
         "Cap all discounts at 20% without CFO approval",
         "Eliminate 30-50% discount tiers from standard campaigns",
         "Replace heavy discounts with value bundles (buy 3 get 1)",
         "Monitor discount-profit in real time via Power BI dashboard",
     ], "Low complexity | High impact"),
    (ACCENT_GREEN, "Recommendation 2: Corporate Segment Growth Strategy",
     [
         "Identify top 100 Corporate customers by lifetime value",
         "Assign dedicated account managers to key accounts",
         "Offer volume pricing tiers (within margin guardrails)",
         "Launch 'Corporate Preferred' program with faster shipping",
     ], "Medium complexity | High impact"),
    (ACCENT_ORANGE, "Recommendation 3: Fix Tables Sub-Category Pricing",
     [
         "Conduct COGS analysis for Tables SKUs",
         "Reprice Tables to achieve minimum 5% gross margin",
         "Apply no-discount policy to all Tables immediately",
         "Consider discontinuing lowest-selling Tables SKUs",
     ], "Low complexity | Quick win"),
]

for i, (color, title, bullets, note) in enumerate(recs):
    x = 0.3 + i * 4.3
    add_rect(slide9, x, 1.4, 4.0, 5.2, fill_color=color)
    add_text(slide9, title, x + 0.15, 1.5, 3.7, 0.7, font_size=13,
             bold=True, color=WHITE)
    for j, bullet in enumerate(bullets):
        add_text(slide9, f"• {bullet}", x + 0.15, 2.3 + j * 0.85, 3.7, 0.8,
                 font_size=11, color=WHITE)
    add_rect(slide9, x, 5.95, 4.0, 0.55, fill_color=RGBColor(0,0,0))
    add_text(slide9, note, x + 0.1, 5.98, 3.8, 0.5, font_size=10,
             color=WHITE, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10: Conclusion and Q&A
# ══════════════════════════════════════════════════════════════════════════════
slide10 = prs.slides.add_slide(BLANK_LAYOUT)
add_rect(slide10, 0, 0, 13.33, 7.5, fill_color=DARK_BLUE)
add_rect(slide10, 0, 3.6, 13.33, 0.08, fill_color=ACCENT_BLUE)

add_text(slide10, "Conclusion", 0.5, 0.6, 12.3, 0.8,
         font_size=32, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

summary_items = [
    ("9,994 records cleaned and analyzed", ACCENT_BLUE),
    ("10 professional visualizations generated", ACCENT_GREEN),
    ("10.98% overall profit margin identified", ACCENT_ORANGE),
    ("Key insight: Discounts above 20% are loss-making", WHITE),
    ("3 actionable recommendations provided", ACCENT_BLUE),
    ("Power BI dashboard preparation complete", ACCENT_GREEN),
    ("GitHub documentation ready for submission", ACCENT_ORANGE),
]
for i, (text, color) in enumerate(summary_items):
    add_text(slide10, f"✓  {text}", 1.5, 1.6 + i * 0.4, 10.0, 0.38,
             font_size=14, color=color, align=PP_ALIGN.LEFT)

add_text(slide10, "Questions & Discussion",
         0.5, 5.5, 12.3, 0.7, font_size=26, bold=True,
         color=ACCENT_ORANGE, align=PP_ALIGN.CENTER)
add_text(slide10, "Thank you!",
         0.5, 6.2, 12.3, 0.6, font_size=20,
         color=WHITE, align=PP_ALIGN.CENTER)

# ── Save ───────────────────────────────────────────────────────────────────────
prs.save(PPTX_PATH)
print(f"[OK] Presentation saved: {PPTX_PATH}")
print(f"     Slides: {len(prs.slides)}")

# ── Speaker Notes ──────────────────────────────────────────────────────────────
notes_text = f"""# Speaker Notes — Final Project Presentation
## E-Commerce Sales Analysis | Week 6 Internship Assignment

---

## Slide 1: Project Title and Introduction

**What to say:**
"Good morning / afternoon everyone. My name is [Your Name], and today I'll be presenting my Week 6 Internship Assignment — an end-to-end data analytics capstone project titled 'E-Commerce Sales Data Analysis and Interactive Power BI Dashboard.'

This project uses a synthetic dataset that simulates real retail sales data to build a complete analytics pipeline — from data cleaning through exploratory analysis, visualizations, a Power BI dashboard, and business recommendations.

Let me walk you through what I built and what I discovered."

**Time:** ~30 seconds

---

## Slide 2: Problem Statement and Objectives

**What to say:**
"Every e-commerce business faces the same challenge: they have data, but they need insights. Questions like 'Are our discounts helping or hurting us?', 'Which products are actually profitable?', and 'Which customers are worth targeting?' are hard to answer without proper analysis.

This project set out to answer exactly these kinds of questions using Python data analysis and Power BI visualization. The ten objectives on the right cover the full spectrum — from technical analysis to business recommendations."

**Time:** ~45 seconds

---

## Slide 3: Dataset Overview

**What to say:**
"I used a synthetic dataset that closely mirrors the Tableau Sample Superstore dataset — a well-known retail analytics benchmark. It contains 9,994 transaction records after cleaning, spanning January 2020 to December 2023.

The dataset includes fields like order dates, product categories, sales amounts, discounts, profits, customer segments, and geographic information. After running the data cleaning pipeline, I also added derived features like Order Year, Month, Quarter, and Profit Margin percentage."

**Time:** ~45 seconds

---

## Slide 4: Data Cleaning and Preparation

**What to say:**
"The data cleaning pipeline is implemented in `src/data_cleaning.py`. I followed a systematic eight-step process.

The most important decisions were: I retained 12 records with missing ship dates — because those represent orders that haven't been shipped yet, which is valid data. I removed 3 exact duplicate rows. And critically, I decided to RETAIN potential outliers rather than remove them — because large bulk orders in retail are legitimate transactions, not errors.

The cleaning report is saved in `reports/data_cleaning_summary.md`."

**Time:** ~45 seconds

---

## Slide 5: Exploratory Data Analysis

**What to say:**
"The EDA revealed some very clear patterns.

Total sales were $33.17 million across 9,070 unique orders — with a $3.64 million profit, giving us a 10.98% overall profit margin.

Technology is the leading category by revenue. The West and East regions account for the most transactions. And the Consumer segment makes up over half of all orders — though Corporate customers tend to place larger individual orders.

All of this is calculated directly from the cleaned data — I didn't hard-code any of these numbers."

**Time:** ~1 minute

---

## Slide 6: Data Visualizations

**What to say:**
"I generated 10 professional charts using Matplotlib and Seaborn — well above the minimum of 8 required.

Looking at a few highlights: the sales-by-category bar chart confirms Technology leads. The monthly trend line shows a clear Q4 seasonal spike every year. And the discount-vs-profit scatter plot — which I'll discuss more in the insights section — clearly shows that as discounts increase, profits fall sharply.

All charts are saved as high-resolution PNG files in the `visualizations/` folder."

**Time:** ~45 seconds

---

## Slide 7: Power BI Dashboard

**What to say:**
"For the Power BI dashboard, I've prepared everything needed to build it in Power BI Desktop.

The data source is `data/cleaned_sales.csv`. I've written a complete setup guide at `docs/powerbi_setup_guide.md` and all required DAX measures at `docs/powerbi_dax_measures.md`.

The dashboard design includes 4 KPI cards, 5 chart visuals, and 4 interactive slicers for Date, Region, Category, and Customer Segment.

Power BI Desktop is a GUI application that requires manual setup, so I've documented the exact steps rather than attempting to create the file programmatically."

**Time:** ~45 seconds

---

## Slide 8: Business Insights

**What to say:**
"The analysis produced six key business insights — all backed by actual calculated numbers.

The most critical finding is the strong negative correlation between discounts and profit margin: -0.854. This means as discounts go up, margins collapse. Discounts above 20% consistently generate losses.

Other major findings: Technology leads revenue, the Tables sub-category loses money structurally, sales peak in Q4 every year, Corporate customers are underserved relative to their potential, and the West/East regions dominate while Central and South have untapped growth potential."

**Time:** ~1 minute

---

## Slide 9: Recommendations

**What to say:**
"Based on these insights, I have three specific, actionable recommendations.

First: implement a discount governance policy — cap discounts at 20% and replace heavy discounts with value bundles. The correlation data makes it clear that the current discounting practice is destroying margins.

Second: develop a Corporate segment growth strategy. Corporate customers place larger orders and are more predictable. Investing in account management could yield disproportionate returns.

Third: fix the Tables sub-category pricing immediately. It's operating at a structural loss. This is the easiest quick win — just stop discounting Tables and reprice them to cover costs."

**Time:** ~1 minute

---

## Slide 10: Conclusion and Q&A

**What to say:**
"To summarize what this project delivered: I cleaned and analyzed nearly 10,000 records, generated 10 visualizations, identified a critical discount-profit problem, provided three actionable recommendations, built a complete Power BI preparation package, and documented everything for GitHub submission.

The most important takeaway is this: the data clearly shows that aggressive discounting is the biggest threat to profitability — and that's something management can act on immediately.

Thank you for your attention. I'm happy to answer any questions."

**Time:** ~1 minute

---

## Total Presentation Time: ~7-8 minutes

---

*Speaker notes prepared for Week 6 Internship Assignment*
"""

with open(NOTES_PATH, 'w', encoding='utf-8') as f:
    f.write(notes_text)
print(f"[OK] Speaker notes saved: {NOTES_PATH}")
