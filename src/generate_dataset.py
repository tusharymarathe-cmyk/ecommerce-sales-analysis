"""
generate_dataset.py
-------------------
Generates a realistic synthetic Sample Superstore-style dataset for the
E-Commerce Sales Analysis project.

NOTE: This is SYNTHETIC (artificially generated) data created because the
original Tableau Sample Superstore dataset requires manual download from
Tableau's website. All statistics and business insights derived from this
data are based on synthetic records and should NOT be presented as
real-world findings.

Dataset Source: Synthetically generated using NumPy and Pandas random
generators, calibrated to match the statistical properties of publicly
available retail sales datasets.

Rows: 9,994 (matching the typical Superstore dataset size)
Columns: 21
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ── Configuration ─────────────────────────────────────────────────────────────
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_sales_data.csv')
N_ROWS = 9994

# ── Reference Data ─────────────────────────────────────────────────────────────
REGIONS = {
    'East': ['New York', 'Philadelphia', 'Boston', 'Washington DC', 'Baltimore',
             'Pittsburgh', 'Providence', 'Hartford', 'Burlington', 'Manchester'],
    'West': ['Los Angeles', 'San Francisco', 'Seattle', 'Portland', 'Denver',
             'Las Vegas', 'Phoenix', 'Salt Lake City', 'Albuquerque', 'Tucson'],
    'Central': ['Chicago', 'Dallas', 'Houston', 'Minneapolis', 'St. Louis',
                'Kansas City', 'Memphis', 'New Orleans', 'Oklahoma City', 'Omaha'],
    'South': ['Miami', 'Atlanta', 'Charlotte', 'Nashville', 'Tampa',
              'Jacksonville', 'Louisville', 'Richmond', 'Raleigh', 'Columbia']
}

REGION_STATES = {
    'East': ['New York', 'Pennsylvania', 'Massachusetts', 'Virginia', 'Maryland',
             'Connecticut', 'Rhode Island', 'Vermont', 'New Hampshire', 'Maine'],
    'West': ['California', 'Washington', 'Oregon', 'Colorado', 'Nevada',
             'Arizona', 'Utah', 'New Mexico', 'Montana', 'Idaho'],
    'Central': ['Illinois', 'Texas', 'Minnesota', 'Missouri', 'Kansas',
                'Tennessee', 'Louisiana', 'Oklahoma', 'Nebraska', 'Iowa'],
    'South': ['Florida', 'Georgia', 'North Carolina', 'Alabama', 'South Carolina',
              'Mississippi', 'Arkansas', 'Kentucky', 'Virginia', 'Delaware']
}

SEGMENTS = ['Consumer', 'Corporate', 'Home Office']
SEGMENT_WEIGHTS = [0.52, 0.30, 0.18]

SHIP_MODES = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
SHIP_WEIGHTS = [0.60, 0.20, 0.15, 0.05]

CATEGORIES = {
    'Furniture': {
        'Bookcases': {'base_price': 350, 'margin': 0.05},
        'Chairs': {'base_price': 280, 'margin': 0.14},
        'Furnishings': {'base_price': 65, 'margin': 0.18},
        'Tables': {'base_price': 450, 'margin': -0.05},
    },
    'Office Supplies': {
        'Appliances': {'base_price': 160, 'margin': 0.18},
        'Art': {'base_price': 22, 'margin': 0.24},
        'Binders': {'base_price': 35, 'margin': 0.20},
        'Envelopes': {'base_price': 16, 'margin': 0.28},
        'Fasteners': {'base_price': 9, 'margin': 0.30},
        'Labels': {'base_price': 13, 'margin': 0.32},
        'Paper': {'base_price': 48, 'margin': 0.35},
        'Storage': {'base_price': 95, 'margin': 0.15},
        'Supplies': {'base_price': 55, 'margin': 0.04},
    },
    'Technology': {
        'Accessories': {'base_price': 120, 'margin': 0.20},
        'Copiers': {'base_price': 2200, 'margin': 0.38},
        'Machines': {'base_price': 1200, 'margin': 0.15},
        'Phones': {'base_price': 380, 'margin': 0.17},
    }
}

PRODUCTS = {}
for cat, subcats in CATEGORIES.items():
    for subcat, props in subcats.items():
        n_products = random.randint(8, 20)
        PRODUCTS[subcat] = []
        for i in range(n_products):
            pname = f"{subcat} Item {i+1:03d}"
            PRODUCTS[subcat].append({
                'name': pname,
                'id': f"Prod-{cat[:3].upper()}-{subcat[:3].upper()}-{i+1:04d}",
                'base_price': props['base_price'] * np.random.uniform(0.6, 1.8),
                'margin': props['margin'] + np.random.uniform(-0.05, 0.05)
            })

# ── Date Generation ────────────────────────────────────────────────────────────
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2023, 12, 31)

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def ship_date(order_date, ship_mode):
    delays = {
        'Same Day': 0,
        'First Class': random.randint(1, 3),
        'Second Class': random.randint(3, 6),
        'Standard Class': random.randint(5, 10)
    }
    return order_date + timedelta(days=delays[ship_mode])

# ── Seasonal multiplier ────────────────────────────────────────────────────────
def seasonal_weight(month):
    """Higher sales in Q4 (holiday season) and Q2."""
    weights = {
        1: 0.75, 2: 0.70, 3: 0.85, 4: 0.90,
        5: 0.95, 6: 1.00, 7: 0.85, 8: 0.80,
        9: 0.95, 10: 1.05, 11: 1.25, 12: 1.35
    }
    return weights.get(month, 1.0)

# ── Generate Records ───────────────────────────────────────────────────────────
records = []
order_counter = 1000
customer_pool = [f"CUST-{i:05d}" for i in range(1, 801)]

for i in range(N_ROWS):
    # Region and city
    region = np.random.choice(list(REGIONS.keys()), p=[0.28, 0.30, 0.22, 0.20])
    city = random.choice(REGIONS[region])
    state = random.choice(REGION_STATES[region])

    # Date
    order_dt = random_date(START_DATE, END_DATE)
    # Apply seasonal bias by oversampling high-season months
    if random.random() < (seasonal_weight(order_dt.month) - 0.7):
        order_dt = random_date(START_DATE, END_DATE)
    ship_mode = np.random.choice(SHIP_MODES, p=SHIP_WEIGHTS)
    ship_dt = ship_date(order_dt, ship_mode)

    # Order ID (multiple rows can share an order ID)
    if i == 0 or random.random() < 0.70:
        order_counter += 1
    order_id = f"CA-{order_dt.year}-{order_counter:07d}"

    # Customer
    customer_id = random.choice(customer_pool)
    segment = np.random.choice(SEGMENTS, p=SEGMENT_WEIGHTS)

    # Product
    cat = random.choice(list(CATEGORIES.keys()))
    subcat = random.choice(list(CATEGORIES[cat].keys()))
    product = random.choice(PRODUCTS[subcat])

    # Sales and profit
    quantity = np.random.randint(1, 15)
    unit_price = product['base_price'] * np.random.uniform(0.85, 1.15)
    discount = np.random.choice([0, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
                                 p=[0.40, 0.18, 0.12, 0.10, 0.08, 0.05, 0.04, 0.01, 0.01, 0.01])
    sales = round(unit_price * quantity * (1 - discount), 2)
    base_margin = product['margin']
    # Higher discounts erode margin
    effective_margin = base_margin - (discount * 1.2)
    profit = round(sales * effective_margin * np.random.uniform(0.85, 1.15), 2)

    records.append({
        'Row ID': i + 1,
        'Order ID': order_id,
        'Order Date': order_dt.strftime('%d/%m/%Y'),
        'Ship Date': ship_dt.strftime('%d/%m/%Y'),
        'Ship Mode': ship_mode,
        'Customer ID': customer_id,
        'Customer Name': f"Customer {customer_id}",
        'Segment': segment,
        'Country': 'United States',
        'City': city,
        'State': state,
        'Postal Code': f"{random.randint(10000, 99999)}",
        'Region': region,
        'Product ID': product['id'],
        'Category': cat,
        'Sub-Category': subcat,
        'Product Name': product['name'],
        'Sales': sales,
        'Quantity': quantity,
        'Discount': discount,
        'Profit': profit
    })

df = pd.DataFrame(records)

# Introduce a small number of realistic data quality issues for cleaning exercise
# 1. A few missing values in Ship Date (order not yet shipped)
missing_ship_idx = df.sample(n=12, random_state=42).index
df.loc[missing_ship_idx, 'Ship Date'] = None

# 2. A couple of duplicate rows
dup_rows = df.sample(n=3, random_state=7)
df = pd.concat([df, dup_rows], ignore_index=True)

# 3. Shuffle
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"[OK] Dataset generated successfully!")
print(f"   Rows: {len(df):,}")
print(f"   Columns: {len(df.columns)}")
print(f"   Saved to: {os.path.abspath(OUTPUT_PATH)}")
print(f"\n   IMPORTANT: This is SYNTHETIC data for educational purposes only.")
print(f"   Column names: {list(df.columns)}")
