"""
analysis.py
-----------
Master end-to-end data analytics pipeline runner for Week 6 Internship Assignment.
Student: Tushar Marathe | Organization: Internova | Domain: Data Analytics

Orchestrates:
1. Data Cleaning & Feature Engineering (src/data_cleaning.py)
2. Statistical EDA & Visualizations (src/eda_analysis.py)
3. Jupyter Notebook Building & Full Execution (src/build_executed_notebook.py)
4. Comprehensive 12-Page PDF Report Generation (src/create_report.py)
5. Executive PowerPoint Presentation Generation (src/create_presentation.py)
6. Automated Quality Assurance & Verification Suite (tests/run_tests.py)

Usage:
    python src/analysis.py
"""

import os
import sys
import subprocess
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_EXE = sys.executable

STEPS = [
    ("Step 1: Data Cleaning & Validation", os.path.join(BASE_DIR, 'src', 'data_cleaning.py')),
    ("Step 2: EDA & Visualization Generation", os.path.join(BASE_DIR, 'src', 'eda_analysis.py')),
    ("Step 3: Jupyter Notebook Build & Execution", os.path.join(BASE_DIR, 'src', 'build_executed_notebook.py')),
    ("Step 4: Executive PDF Report Generation", os.path.join(BASE_DIR, 'src', 'create_report.py')),
    ("Step 5: PowerPoint Presentation Generation", os.path.join(BASE_DIR, 'src', 'create_presentation.py')),
    ("Step 6: Quality Assurance Test Suite", os.path.join(BASE_DIR, 'tests', 'run_tests.py')),
]

def main():
    print("=" * 70)
    print("INTERNOVA DATA ANALYTICS INTERNSHIP — WEEK 6 FINAL PROJECT")
    print("STUDENT: Tushar Marathe | ASSIGNMENT: Week 6 Git, GitHub & Final Project")
    print("=" * 70)
    print(f"Project Root Directory: {BASE_DIR}\n")

    overall_start = time.time()
    success_count = 0

    for step_num, (step_name, script_path) in enumerate(STEPS, 1):
        print(f"\n[{step_num}/{len(STEPS)}] Running: {step_name}...")
        print("-" * 50)
        start_time = time.time()

        proc = subprocess.run(
            [PYTHON_EXE, script_path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        elapsed = time.time() - start_time

        if proc.returncode == 0:
            print(proc.stdout.strip())
            print(f"[PASS] {step_name} completed in {elapsed:.2f}s")
            success_count += 1
        else:
            print(f"[FAIL] {step_name} failed with return code {proc.returncode}!")
            if proc.stdout:
                print("--- Output ---:\n", proc.stdout.strip())
            if proc.stderr:
                print("--- Error ---:\n", proc.stderr.strip())
            sys.exit(proc.returncode)

    total_elapsed = time.time() - overall_start
    print("\n" + "=" * 70)
    print(f"PIPELINE RUN COMPLETE: {success_count}/{len(STEPS)} steps passed in {total_elapsed:.2f}s")
    print("ALL DELIVERABLES SUCCESSFULLY GENERATED AND VERIFIED")
    print("=" * 70)


if __name__ == '__main__':
    main()
