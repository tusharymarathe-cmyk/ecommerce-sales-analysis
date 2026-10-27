# Internova Week 6 Final Assignment — Submission Links & Instructions

**Student Name:** Tushar Marathe  
**Internship Organization:** Internova  
**Domain:** Data Analytics  
**Assignment:** Week 6 — Git, GitHub & Final Data Analytics Project  
**Maximum Marks:** 100 | **Evaluation Period:** 7 Days  

---

## Submission Options Overview

The Internova assignment portal permits submission via any of the following three options. All materials are fully prepared and verified for each option below:

---

### OPTION 1: GitHub Repository Link (Recommended)

Submit the public GitHub repository URL containing the entire source code, dataset, executed notebook, reports, and presentations:

```text
https://github.com/tusharymarathe-cmyk/ecommerce-sales-analysis
```

#### Steps to Sync Latest Local Commits to GitHub:
If you need to push any recent updates to GitHub, open your terminal / PowerShell in the project directory and run:

```bash
cd "C:\Users\TUSHAR MARATHE\OneDrive\Documents\ai pROJECT\ecommerce-sales-analysis"
git status
git add .
git commit -m "Finalize Week 6 internship assignment deliverables, executed notebook, and submission checklist"
git push origin main
```

> **Note on GitHub Authentication:** If prompted for GitHub credentials during `git push`, use your GitHub Personal Access Token (PAT) with `repo` scope or sign in via GitHub Credential Manager.

---

### OPTION 2: Google Drive Link

If submitting via Google Drive:
1. Locate the project folder on your local machine:
   ```text
   C:\Users\TUSHAR MARATHE\OneDrive\Documents\ai pROJECT\ecommerce-sales-analysis
   ```
2. Compress the folder into a `.zip` file:
   - Right-click `ecommerce-sales-analysis` → **Compress to ZIP file** (or `ecommerce-sales-analysis-Tushar-Marathe.zip`).
3. Upload the `.zip` file to your Google Drive.
4. Set link sharing to **"Anyone with the link can view"**.
5. Paste the shareable Google Drive link into the Internova submission portal.

---

### OPTION 3: Direct PDF Upload

If the submission form requires uploading a single comprehensive document:
Upload the generated 12-page formal project report directly:

- **File Path:**
  ```text
  reports/final_project_report.pdf
  ```
- **Alternate Path:**
  ```text
  reports/Final_Data_Analytics_Project_Report.pdf
  ```
- **File Size:** ~1.01 MB (comfortably below standard 10 MB portal upload limits).
- **Contents:** Fully self-contained formal report including student metadata, executive summary, KPI tables, data cleaning methodology, 10 embedded high-resolution visualizations, statistical findings, Power BI architecture, and strategic recommendations.

---

## Summary of Deliverable Files for Submission

| Deliverable | File Path | Description |
|---|---|---|
| **Main Documentation** | `README.md` | Comprehensive GitHub project overview |
| **Executed Notebook** | `notebooks/final_data_analytics_project.ipynb` | Jupyter notebook with 100% executed cells, tables & plots |
| **Alternate Notebook** | `notebooks/EDA_Analysis.ipynb` | Alternate executed notebook |
| **Cleaned Dataset** | `data/cleaned_sales.csv` | 9,994 validated records, 26 features |
| **Raw Dataset** | `data/raw/raw_sales_data.csv` | 9,997 raw records |
| **Final PDF Report** | `reports/final_project_report.pdf` | 12-page executive publication-ready PDF report (1.01 MB) |
| **Presentation** | `presentation/final_project_presentation.pptx` | 10 widescreen executive slides |
| **Speaker Notes** | `presentation/Speaker_Notes.md` | Slide-by-slide speech script |
| **Master Pipeline** | `src/analysis.py` | End-to-end Python pipeline runner |
| **Cleaning Pipeline** | `src/data_cleaning.py` | Python data cleaning pipeline |
| **Power BI DAX** | `power_bi/dax_measures.md` | 18 production DAX formulas |
| **Power BI Design** | `power_bi/dashboard_design.md` | 12-column layout and coordinate guide |
| **Business Insights** | `reports/business_insights.md` | 5 empirical insights + 4 practical recommendations |
| **Submission Audit** | `submission/submission_checklist.md` | Task-by-task verification matrix |
