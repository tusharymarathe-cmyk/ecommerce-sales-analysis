# Power BI Executive Dashboard Layout & Design Guide
## Sales and E-Commerce Performance Analytics Dashboard

**Student:** Tushar Marathe | **Organization:** Internova | **Domain:** Data Analytics  
**Canvas Resolution:** 1920 × 1080 (16:9 Widescreen)  
**Target Design Philosophy:** Modern Executive BI (Clean container cards, subtle drop shadows, deliberate data density, high contrast readability).

---

## 1. Design System & Palette

| Element | Color Name | Hex Code | Purpose |
|---|---|---|---|
| **Primary Brand** | Deep Corporate Navy | `#1E3A8A` | Headers, primary bar series, KPI text |
| **Accent Positive** | Emerald Green | `#10B981` | Profit values, positive margins, KPI badges |
| **Accent Alert** | Crimson Red | `#EF4444` | Loss regions, high discount alerts, negative profit |
| **Accent Warning** | Warm Amber | `#F59E0B` | Medium margin warnings, seasonal markers |
| **Neutral Canvas** | Soft Slate Gray | `#F8FAFC` | Main canvas background |
| **Container Card** | Pure White | `#FFFFFF` | Visual container card background |
| **Border / Shadow** | Light Slate | `#E2E8F0` | Card borders (1px) with 10% opacity soft shadow |
| **Text Primary** | Dark Slate | `#0F172A` | Visual titles, major metric labels |
| **Text Secondary** | Muted Slate | `#64748B` | Subtitles, axis tick labels, footnotes |

---

## 2. 12-Column Grid Layout Architecture

The canvas is structured into four functional zones:

```text
+----------------------------------------------------------------------------------------------------+
| ZONE 1: HEADER & METADATA BANNER (Height: 80px | Width: 1880px)                                    |
| Title: Sales and E-Commerce Performance Analytics Dashboard | Internova - Week 6 Final Project     |
| Last Refreshed: [Dynamic] | Student: Tushar Marathe                                                |
+----------------------------------------------------------------------------------------------------+
| ZONE 2: GLOBAL SLICERS RIBBON (Height: 60px | Width: 1880px)                                       |
| [ Order Date Slider ]  [ Region: All/W/E/C/S ]  [ Category: All/Tech/Off/Furn ]  [ Segment: All ]  |
+----------------------------------------------------------------------------------------------------+
| ZONE 3: EXECUTIVE KPI BANNER (Height: 120px | 5 Equal Width Cards: 360px each)                     |
| +----------------+ +----------------+ +----------------+ +----------------+ +--------------------+ |
| | Total Sales    | | Total Profit   | | Profit Margin  | | Total Orders   | | Avg Order Value    | |
| | $33.17M        | | $3.64M         | | 10.98%         | | 9,070          | | $3,657.22          | |
| +----------------+ +----------------+ +----------------+ +----------------+ +--------------------+ |
+----------------------------------------------------------------------------------------------------+
| ZONE 4: ANALYTIC VISUAL TILES (Height: 740px)                                                      |
|                                                                                                    |
| +-----------------------------------------------+ +----------------------------------------------+ |
| | Visual 1: Monthly Sales & Profit Trend        | | Visual 2: Sales vs Profit by Category        | |
| | (Line & Clustered Column Chart - 920x350)     | | (Clustered Bar Chart - 920x350)              | |
| +-----------------------------------------------+ +----------------------------------------------+ |
|                                                                                                    |
| +------------------------+ +------------------------+ +------------------------------------------+ |
| | Visual 3: Profit by    | | Visual 4: Sales by     | | Visual 5: Top 10 Revenue Products        | |
| | Region (Bar - 600x360) | | Segment (Donut - 600)  | | (Horizontal Bar with Margin - 640x360)   | |
| +------------------------+ +------------------------+ +------------------------------------------+ |
+----------------------------------------------------------------------------------------------------+
```

---

## 3. Visual Container Geometry & Coordinates

| Visual Container | Type | X | Y | Width | Height | Visual Setup |
|---|---|---|---|---|---|---|
| **Header Banner** | Text / Shape | 20 | 20 | 1880 | 70 | Text Box: 20pt Bold Navy |
| **Slicer 1: Date** | Slicer (Between) | 20 | 100 | 440 | 50 | Field: `cleaned_sales[Order Date]` |
| **Slicer 2: Region** | Slicer (Tile) | 480 | 100 | 440 | 50 | Field: `cleaned_sales[Region]` |
| **Slicer 3: Category** | Slicer (Tile) | 940 | 100 | 440 | 50 | Field: `cleaned_sales[Category]` |
| **Slicer 4: Segment** | Slicer (Tile) | 1400 | 100 | 500 | 50 | Field: `cleaned_sales[Segment]` |
| **KPI Card 1** | Card (New) | 20 | 165 | 360 | 110 | Measure: `[Total Sales]` |
| **KPI Card 2** | Card (New) | 400 | 165 | 360 | 110 | Measure: `[Total Profit]` |
| **KPI Card 3** | Card (New) | 780 | 165 | 360 | 110 | Measure: `[Profit Margin %]` |
| **KPI Card 4** | Card (New) | 1160 | 165 | 360 | 110 | Measure: `[Total Orders]` |
| **KPI Card 5** | Card (New) | 1540 | 165 | 360 | 110 | Measure: `[Average Order Value]` |
| **Visual 1** | Line + Column | 20 | 290 | 920 | 360 | X: Order Date, Col: Sales, Line: Profit |
| **Visual 2** | Clustered Bar | 960 | 290 | 940 | 360 | Y: Category, X: Sales & Profit |
| **Visual 3** | Bar Chart | 20 | 670 | 600 | 380 | Y: Region, X: Total Profit |
| **Visual 4** | Donut Chart | 640 | 670 | 600 | 380 | Legend: Segment, Value: Total Sales |
| **Visual 5** | Bar Chart | 1260 | 670 | 640 | 380 | Y: Product Name (Top 10), X: Total Sales |

---

## 4. Visual Configuration & Styling Rules

### Rule 1: Numeric Formatting
- All Sales, Profit, and AOV figures MUST be formatted with currency prefix `$` and thousand separators (e.g., `$33,170,960`).
- Profit Margins MUST display exactly one decimal place (`11.0%`).
- Quantities and Counts MUST be formatted as whole numbers (`9,070`).

### Rule 2: Title & Typography Hierarchy
- Canvas Title: Segoe UI / Arial, 20pt Bold.
- Visual Titles: Segoe UI / Arial, 13pt Semi-Bold, `#0F172A`.
- Data Callouts (KPIs): Segoe UI, 28pt Bold.
- Axis & Legend Labels: Segoe UI, 9pt Regular, `#64748B`.

### Rule 3: Cross-Filtering & Interaction Settings
- In the **Format → Edit Interactions** menu:
  - Slicers MUST cross-filter all 5 KPI cards and all 5 visual charts.
  - Clicking on a Category bar (e.g. Technology) in Visual 2 MUST filter Visual 1, Visual 3, Visual 4, and Visual 5.
  - Clicking on a Segment slice in Visual 4 MUST highlight regional and category distributions without resetting date filters.

---

## 5. Validation and Acceptance Test Scenarios

| Test Case | Interaction Action | Expected Outcome |
|---|---|---|
| **TC-01: Baseline Load** | Open report with all filters set to "All" | Total Sales = $33.17M, Profit = $3.64M, Margin = 10.98% |
| **TC-02: Region Filter** | Select `Region = "West"` | Total Sales = $9.89M, Profit = $1.12M, Margin = 11.3% |
| **TC-03: Category Filter**| Select `Category = "Furniture"` | Exposes lower overall profit margin (~8.1%) |
| **TC-04: Date Zoom** | Adjust date slider to `2023-01-01` to `2023-12-31` | Displays FY2023 full-year figures ($9.4M Sales) |
| **TC-05: Product Tooltip** | Hover cursor over Top 1 product | Displays Product Name, Sales, Profit, and Margin % |
