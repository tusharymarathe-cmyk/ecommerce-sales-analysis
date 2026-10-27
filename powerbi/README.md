# Power BI Dashboard Specification & Implementation Guide
## Sales and E-Commerce Performance Analytics Dashboard

**Student:** Tushar Marathe  
**Organization:** Internova  
**Domain:** Data Analytics  
**Assignment:** Week 6 Final Project  

---

## 1. Executive Dashboard Overview

The **Sales and E-Commerce Performance Analytics Dashboard** is engineered to provide executive leadership and operational managers with real-time, interactive insights into top-line revenue, bottom-line profitability, regional performance, customer behavior, and discounting risk.

### Core Architecture
- **Primary Data Source:** `data/cleaned_sales.csv` (and `data/processed/cleaned_sales.csv`)
- **Row Count:** 9,994 transaction line items
- **Temporal Span:** January 1, 2020 — December 31, 2023 (4 Full Operating Years)
- **Granularity:** Line-item transaction level

---

## 2. Dashboard Status & Manual Action Notice

> **⚠️ Formal Status Notice:**  
> Microsoft Power BI Desktop is installed on the local system (`Microsoft.MicrosoftPowerBIDesktop_8wekyb3d8bbwe`). However, Microsoft Power BI Desktop does not support headless CLI automation for generating proprietary binary `.pbix` files.  
> As required by the assignment guidelines:
> - No fake or renamed `.pbix` files are generated.
> - All required data models, DAX measures, layout blueprints, step-by-step import instructions, and verification checklists are prepared and documented below.
> - The final interactive dashboard must be opened and saved directly in Microsoft Power BI Desktop by following the steps in Section 6.

---

## 3. Core KPI Cards Specification

The dashboard incorporates **5 high-impact KPI cards** across the top banner:

| KPI Card | Formula / DAX Measure | Target Format | Business Purpose |
|---|---|---|---|
| **Total Sales** | `[Total Sales]` | Currency (`$#,##0`) | Overall gross revenue volume |
| **Total Profit** | `[Total Profit]` | Currency (`$#,##0`) | Net bottom-line operating income |
| **Profit Margin %** | `[Profit Margin %]` | Percentage (`0.0%`) | Operating profitability efficiency |
| **Total Orders** | `[Total Orders]` | Integer (`#,##0`) | Total unique customer orders fulfilled |
| **Average Order Value** | `[Average Order Value]` | Currency (`$#,##0.00`) | Average ticket size per order transaction |

---

## 4. Visualizations & Visual Specifications

The dashboard integrates **5 complementary visualization tiles**:

1. **Monthly Sales Trend (Jan 2020 – Dec 2023)**
   - *Type:* Line and Clustered Column Chart
   - *X-Axis:* `cleaned_sales[Order Date]` (Hierarchy: Year, Month)
   - *Column Values:* `[Total Sales]`
   - *Line Values:* `[Total Profit]`
   - *Purpose:* Tracks seasonal holiday surges (notably the 34% Q4 demand spike).

2. **Sales and Profitability by Product Category**
   - *Type:* Clustered Bar Chart
   - *Y-Axis:* `cleaned_sales[Category]` (Technology, Office Supplies, Furniture)
   - *X-Axis:* `[Total Sales]`, `[Total Profit]`
   - *Purpose:* Directly contrasts volume leadership with margin generation.

3. **Regional Profit Performance**
   - *Type:* Clustered Horizontal Bar / Map
   - *Y-Axis:* `cleaned_sales[Region]` (West, East, Central, South)
   - *X-Axis:* `[Total Profit]`
   - *Color Saturation:* By `[Profit Margin %]`
   - *Purpose:* Identifies regional profit dominance (West & East generate ~60% of profits).

4. **Sales Distribution by Customer Segment**
   - *Type:* Donut Chart
   - *Legend:* `cleaned_sales[Segment]` (Consumer, Corporate, Home Office)
   - *Values:* `[Total Sales]`
   - *Detail Labels:* Category & Percentage of Total
   - *Purpose:* Visualizes portfolio balance (Consumer 52.1%, Corporate 30.0%, Home Office 18.0%).

5. **Top 10 Products by Revenue & Margin**
   - *Type:* Clustered Horizontal Bar Chart
   - *Y-Axis:* `cleaned_sales[Product Name]` (Filtered to Top 10 by `[Total Sales]`)
   - *X-Axis:* `[Total Sales]`
   - *Tooltip:* `[Total Profit]`, `[Profit Margin %]`
   - *Purpose:* Isolates high-ticket drivers like enterprise copiers and servers.

---

## 5. Interactive Slicers & Cross-Filtering

The dashboard features **4 coordinated global slicers**:

1. **Date Range Slicer:** Between slider on `cleaned_sales[Order Date]` (2020-01-01 to 2023-12-31).
2. **Region Slicer:** Multi-select dropdown or horizontal tiles (`Central`, `East`, `South`, `West`).
3. **Category Slicer:** Multi-select tiles (`Furniture`, `Office Supplies`, `Technology`).
4. **Customer Segment Slicer:** Multi-select buttons (`Consumer`, `Corporate`, `Home Office`).

---

## 6. Step-by-Step Power BI Desktop Construction Guide

### Step 1: Open and Import Data
1. Launch **Microsoft Power BI Desktop** from your Windows Start Menu.
2. In the Welcome Screen or Home Ribbon, select **Get Data → Text/CSV**.
3. Browse to `c:\Users\TUSHAR MARATHE\OneDrive\Documents\ai pROJECT\ecommerce-sales-analysis\data\cleaned_sales.csv`.
4. Review the data preview and click **Load**.

### Step 2: Create DAX Measures Table
1. On the **Home** ribbon, click **Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Right-click `_Measures` in the Data pane and select **New Measure**.
4. Copy and paste each formula from [`dax_measures.md`](dax_measures.md).

### Step 3: Configure Dashboard Layout
1. Follow the layout grid and coordinate specifications in [`dashboard_design.md`](dashboard_design.md).
2. Set Canvas Background to `#F8FAFC` (Off-white / Slate).
3. Insert visual containers with `#FFFFFF` background, rounded borders (8px), and subtle drop shadows.
4. Add the 5 KPI Cards across the top ribbon ($Y = 100\text{px}$).
5. Place the Slicers in the left sidebar or top filter ribbon.
6. Assemble the 5 visualizations across the center and lower canvas.

### Step 4: Verification Checklist
- [ ] Changing the **Region slicer** (e.g. selecting "West") dynamically updates Total Sales ($9.89M) and Total Profit ($1.12M).
- [ ] Filtering to **Category = Furniture** demonstrates lower margins and exposes the Tables sub-category.
- [ ] The **Date slicer** correctly filters the timeline down to individual quarters and months.
- [ ] All currency figures format cleanly with `$` prefix and commas.

### Step 5: Save Project
- Save the file as `power_bi/Sales_and_Ecommerce_Dashboard.pbix` in this directory.
