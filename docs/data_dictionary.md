# Data Dictionary
## E-Commerce Sales Analysis Project

**Version:** 1.0  
**Last Updated:** October 2026  
**Dataset Type:** Synthetic (Superstore-style retail sales data)

---

## Table of Contents
1. [Overview](#overview)
2. [Column Definitions](#column-definitions)
3. [Business Definitions](#business-definitions)
4. [KPI Definitions](#kpi-definitions)
5. [Categorical Value Glossary](#categorical-value-glossary)

---

## Overview

The dataset simulates a US retail e-commerce company's order-level transaction records spanning January 2020 to December 2023. Each row represents one line item within an order (an order may contain multiple products).

**Grain:** One row = one product line within one order  
**Time Range:** 2020-01-01 to 2023-12-31  
**Geography:** United States (4 regions, 40 cities, 40 states)

---

## Column Definitions

### Identifiers

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| Row ID | Integer | No | Unique integer identifier for each row. Not used in analysis. |
| Order ID | String | No | Identifier for the order. Multiple rows share the same Order ID when an order contains multiple products. Format: `CA-YYYY-NNNNNNN` |
| Customer ID | String | No | Unique identifier for each customer. Format: `CUST-NNNNN` |
| Customer Name | String | No | Display name derived from Customer ID. |
| Product ID | String | No | Unique identifier for each product. Format: `Prod-CAT-SUB-NNNN` |
| Product Name | String | No | Human-readable product name. |

### Temporal Fields

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| Order Date | Date | No | Date the customer placed the order. Format: DD/MM/YYYY in raw file; datetime in cleaned file. |
| Ship Date | Date | **Yes** | Date the order was shipped. NULL for 12 records representing orders not yet shipped. |
| Order Year | Integer | No | Year extracted from Order Date. Range: 2020–2023. *(Derived — cleaned file only)* |
| Order Month | Integer | No | Month number (1–12). *(Derived — cleaned file only)* |
| Order Month Name | String | No | Three-letter month abbreviation (Jan–Dec). *(Derived — cleaned file only)* |
| Order Quarter | Integer | No | Quarter number (1–4). *(Derived — cleaned file only)* |

### Geographic Fields

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| Country | String | No | Country of delivery. All records: "United States" |
| Region | String | No | US geographic region. Values: East, West, Central, South |
| State | String | No | US state name. |
| City | String | No | Delivery city name. |
| Postal Code | String | No | 5-digit US postal code. |

### Operational Fields

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| Ship Mode | String | No | Shipping method. Values: Standard Class, Second Class, First Class, Same Day |
| Segment | String | No | Customer business segment. Values: Consumer, Corporate, Home Office |

### Product Classification

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| Category | String | No | Top-level product category. Values: Technology, Office Supplies, Furniture |
| Sub-Category | String | No | Product sub-category. 17 unique values (see Categorical Value Glossary). |

### Financial Fields

| Column | Type | Nullable | Description | Units |
|--------|------|----------|-------------|-------|
| Sales | Float | No | Revenue from this line item. = Quantity × Unit Price × (1 - Discount) | USD |
| Quantity | Integer | No | Number of units sold. Range: 1–14 | Units |
| Discount | Float | No | Discount rate applied. Range: 0.0 to 0.8 (0% to 80%) | Decimal (0–1) |
| Profit | Float | No | Net profit from this line item. Can be negative. | USD |
| Profit Margin % | Float | No | (Profit / Sales) × 100. *(Derived — cleaned file only)* | Percentage |

---

## Business Definitions

### Sales
**Formula:** `Quantity × Unit Price × (1 - Discount)`  
**Description:** Gross revenue earned from a transaction after applying any discount. Does not include cost of goods sold.

### Profit
**Formula:** `Sales × Effective Margin`  
**Description:** Net profit after deducting cost of goods. Negative profit indicates that the transaction was sold at a loss (common at high discount rates).

### Profit Margin %
**Formula:** `(Profit / Sales) × 100`  
**Description:** Percentage of revenue retained as profit. A 0% margin means the company broke even; negative means a loss.

### Order
**Definition:** A unique `Order ID`. One order can contain multiple rows (products). Use `DISTINCTCOUNT(Order ID)` when counting orders to avoid double-counting.

### Average Order Value
**Formula:** `Total Sales / Number of Unique Orders`  
**Description:** The average revenue generated per order.

---

## KPI Definitions

| KPI | Formula | Business Purpose |
|-----|---------|-----------------|
| Total Sales | `SUM(Sales)` | Total revenue |
| Total Profit | `SUM(Profit)` | Total net earnings |
| Total Quantity | `SUM(Quantity)` | Total units sold |
| Total Orders | `DISTINCTCOUNT(Order ID)` | Number of unique orders placed |
| Profit Margin % | `Total Profit / Total Sales × 100` | Overall profitability rate |
| Average Order Value | `Total Sales / Total Orders` | Revenue efficiency per order |

---

## Categorical Value Glossary

### Segment
| Value | Description |
|-------|-------------|
| Consumer | Individual retail customers (B2C) |
| Corporate | Business customers (B2B, larger volumes) |
| Home Office | Small home-office businesses |

### Region
| Value | Coverage |
|-------|---------|
| East | NY, PA, MA, VA, MD, CT, RI, VT, NH, ME |
| West | CA, WA, OR, CO, NV, AZ, UT, NM, MT, ID |
| Central | IL, TX, MN, MO, KS, TN, LA, OK, NE, IA |
| South | FL, GA, NC, AL, SC, MS, AR, KY, VA, DE |

### Ship Mode
| Value | Typical Delivery | Distribution |
|-------|-----------------|-------------|
| Standard Class | 5–10 days | 60% of orders |
| Second Class | 3–6 days | 20% of orders |
| First Class | 1–3 days | 15% of orders |
| Same Day | Same day | 5% of orders |

### Category & Sub-Category
| Category | Sub-Categories |
|----------|---------------|
| Technology | Accessories, Copiers, Machines, Phones |
| Furniture | Bookcases, Chairs, Furnishings, Tables |
| Office Supplies | Appliances, Art, Binders, Envelopes, Fasteners, Labels, Paper, Storage, Supplies |

### Discount Values Used
| Discount | Meaning |
|----------|---------|
| 0.00 | No discount (40% of records) |
| 0.10 | 10% off |
| 0.15 | 15% off |
| 0.20 | 20% off |
| 0.30 | 30% off |
| 0.40 | 40% off |
| 0.50 | 50% off |
| 0.60–0.80 | Heavy promotional discounts (rare) |

---

*This dictionary was created as part of the Week 6 Internship Assignment.*
