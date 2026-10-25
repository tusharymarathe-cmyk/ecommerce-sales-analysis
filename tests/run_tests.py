"""
run_tests.py - Standalone test runner (no pytest required)
"""
import os, sys, pandas as pd, numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# run_tests.py is in tests/, so go up one level
BASE_DIR = os.path.dirname(BASE_DIR)
CLEAN_PATH = os.path.join(BASE_DIR, 'data', 'cleaned_sales.csv')
RAW_PATH = os.path.join(BASE_DIR, 'data', 'raw_sales_data.csv')

passed = 0
failed = 0

def check(name, condition, detail=''):
    global passed, failed
    if condition:
        print(f'  [PASS] {name}')
        passed += 1
    else:
        print(f'  [FAIL] {name}' + (f' | {detail}' if detail else ''))
        failed += 1

print('=' * 60)
print('E-COMMERCE PROJECT — DATA QUALITY CHECK SUITE')
print('=' * 60)

# Load data
raw = pd.read_csv(RAW_PATH)
clean = pd.read_csv(CLEAN_PATH)
clean['Order Date'] = pd.to_datetime(clean['Order Date'])

print('\n--- Group 1: File Existence ---')
check('Raw file exists', os.path.exists(RAW_PATH))
check('Cleaned file exists', os.path.exists(CLEAN_PATH))
check('Cleaning report exists', os.path.exists(os.path.join(BASE_DIR,'reports','data_cleaning_summary.md')))
check('EDA report exists', os.path.exists(os.path.join(BASE_DIR,'reports','eda_summary.md')))
check('Business insights exists', os.path.exists(os.path.join(BASE_DIR,'reports','business_insights.md')))

print('\n--- Group 2: Dataset Size ---')
check('Raw has >=9000 rows', len(raw) >= 9000, f'Got {len(raw)}')
check('Clean has >=9000 rows', len(clean) >= 9000, f'Got {len(clean)}')
check('Cleaning reduced row count', len(clean) <= len(raw), f'Clean={len(clean)}, Raw={len(raw)}')

print('\n--- Group 3: Required Columns ---')
req_cols = ['Order ID','Order Date','Ship Mode','Customer ID','Segment',
            'Region','Category','Sub-Category','Sales','Quantity','Discount','Profit']
for col in req_cols:
    check(f'Column: {col}', col in clean.columns)

print('\n--- Group 4: Derived Columns ---')
for col in ['Order Year','Order Month','Order Quarter','Profit Margin %']:
    check(f'Derived: {col}', col in clean.columns)

print('\n--- Group 5: Data Quality ---')
check('No exact duplicates', clean.duplicated().sum() == 0, f'{clean.duplicated().sum()} dups remain')
check('Sales all positive', (clean['Sales'] > 0).all(), f"{(clean['Sales'] <= 0).sum()} non-positive")
check('Quantity all positive', (clean['Quantity'] > 0).all())
check('Discount in [0,1]', clean['Discount'].between(0,1).all())
check('Order Date is datetime', pd.api.types.is_datetime64_any_dtype(clean['Order Date']))

print('\n--- Group 6: Business Rules ---')
check('3 categories present', clean['Category'].nunique() == 3, f"Got {clean['Category'].nunique()}")
check('4 regions present', clean['Region'].nunique() == 4, f"Got {clean['Region'].nunique()}")
check('3 segments present', clean['Segment'].nunique() == 3, f"Got {clean['Segment'].nunique()}")
check('Year range 2020-2023', clean['Order Year'].between(2020,2023).all())
check('Month range 1-12', clean['Order Month'].between(1,12).all())
check('Quarter range 1-4', clean['Order Quarter'].between(1,4).all())
check('>=100 unique customers', clean['Customer ID'].nunique() >= 100, f"Got {clean['Customer ID'].nunique()}")
check('>=50 unique products', clean['Product Name'].nunique() >= 50, f"Got {clean['Product Name'].nunique()}")
check('Multiple years in data', clean['Order Year'].nunique() >= 2)
check('>=10 sub-categories', clean['Sub-Category'].nunique() >= 10, f"Got {clean['Sub-Category'].nunique()}")
check('Total sales > 0', clean['Sales'].sum() > 0)

print('\n--- Group 7: Visualizations ---')
viz_dir = os.path.join(BASE_DIR, 'visualizations')
pngs = [f for f in os.listdir(viz_dir) if f.endswith('.png')] if os.path.exists(viz_dir) else []
check('>=8 charts generated', len(pngs) >= 8, f'Found {len(pngs)}')
for i in range(1, 11):
    fname = f'{i:02d}_'
    matching = [f for f in pngs if f.startswith(fname)]
    check(f'Chart {i:02d} exists', len(matching) > 0)

total = passed + failed
print(f'\n{"=" * 60}')
print(f'RESULTS: {passed}/{total} checks passed ({100*passed//total}%)')
if failed > 0:
    print(f'WARNING: {failed} check(s) FAILED — review output above')
else:
    print('ALL CHECKS PASSED')
print('=' * 60)
