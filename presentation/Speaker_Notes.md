# Speaker Notes — Final Project Presentation
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
