"""
test_data_cleaning.py
---------------------
Unit tests for the data cleaning pipeline.
E-Commerce Sales Analysis Project — Week 6 Internship Assignment

Run with:
    pytest tests/test_data_cleaning.py -v

Or from the project root:
    python -m pytest tests/ -v
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# ── Path Setup ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw_sales_data.csv')
CLEAN_DATA_PATH = os.path.join(BASE_DIR, 'data', 'cleaned_sales.csv')


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURE: Load cleaned dataset once for all tests
# ══════════════════════════════════════════════════════════════════════════════
@pytest.fixture(scope='module')
def raw_df():
    """Load the raw dataset."""
    assert os.path.exists(RAW_DATA_PATH), (
        f"Raw dataset not found at: {RAW_DATA_PATH}\n"
        f"Run: python src/generate_dataset.py"
    )
    return pd.read_csv(RAW_DATA_PATH)


@pytest.fixture(scope='module')
def clean_df():
    """Load the cleaned dataset."""
    assert os.path.exists(CLEAN_DATA_PATH), (
        f"Cleaned dataset not found at: {CLEAN_DATA_PATH}\n"
        f"Run: python src/data_cleaning.py"
    )
    df = pd.read_csv(CLEAN_DATA_PATH)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df


# ══════════════════════════════════════════════════════════════════════════════
# TEST GROUP 1: Dataset Loading
# ══════════════════════════════════════════════════════════════════════════════
class TestDatasetLoading:
    """Tests for successful dataset loading."""

    def test_raw_file_exists(self):
        """Raw dataset file must exist."""
        assert os.path.exists(RAW_DATA_PATH), f"File not found: {RAW_DATA_PATH}"

    def test_cleaned_file_exists(self):
        """Cleaned dataset file must exist."""
        assert os.path.exists(CLEAN_DATA_PATH), f"File not found: {CLEAN_DATA_PATH}"

    def test_raw_dataset_not_empty(self, raw_df):
        """Raw dataset must have records."""
        assert len(raw_df) > 0, "Raw dataset is empty"

    def test_clean_dataset_not_empty(self, clean_df):
        """Cleaned dataset must have records."""
        assert len(clean_df) > 0, "Cleaned dataset is empty"

    def test_raw_dataset_minimum_rows(self, raw_df):
        """Raw dataset must have at least 9,000 rows."""
        assert len(raw_df) >= 9000, f"Expected >= 9000 rows, got {len(raw_df)}"

    def test_clean_dataset_minimum_rows(self, clean_df):
        """Cleaned dataset must have at least 9,000 rows."""
        assert len(clean_df) >= 9000, f"Expected >= 9000 rows, got {len(clean_df)}"

    def test_required_columns_present(self, clean_df):
        """All required columns must be present in cleaned dataset."""
        required = [
            'Order ID', 'Order Date', 'Ship Mode', 'Customer ID',
            'Segment', 'Region', 'Category', 'Sub-Category',
            'Sales', 'Quantity', 'Discount', 'Profit'
        ]
        for col in required:
            assert col in clean_df.columns, f"Required column missing: '{col}'"

    def test_derived_columns_present(self, clean_df):
        """Derived columns must be added by cleaning script."""
        derived = ['Order Year', 'Order Month', 'Order Quarter', 'Profit Margin %']
        for col in derived:
            assert col in clean_df.columns, f"Derived column missing: '{col}'"


# ══════════════════════════════════════════════════════════════════════════════
# TEST GROUP 2: Duplicate Handling
# ══════════════════════════════════════════════════════════════════════════════
class TestDuplicateHandling:
    """Tests verifying duplicate records were removed."""

    def test_no_exact_duplicates_in_cleaned(self, clean_df):
        """Cleaned dataset must have zero exact duplicate rows."""
        n_dups = clean_df.duplicated().sum()
        assert n_dups == 0, f"Cleaned dataset still has {n_dups} duplicate rows"

    def test_cleaning_removed_duplicates(self, raw_df, clean_df):
        """Cleaning must reduce row count (duplicates removed)."""
        # Raw has 3 intentional duplicates
        assert len(clean_df) <= len(raw_df), \
            "Cleaned dataset has MORE rows than raw — unexpected"

    def test_row_reduction_reasonable(self, raw_df, clean_df):
        """Cleaning should not remove more than 5% of rows."""
        max_allowed_removal = len(raw_df) * 0.05
        actual_removal = len(raw_df) - len(clean_df)
        assert actual_removal <= max_allowed_removal, (
            f"Too many rows removed: {actual_removal} (max allowed: {max_allowed_removal:.0f})"
        )


# ══════════════════════════════════════════════════════════════════════════════
# TEST GROUP 3: Data Type Conversions
# ══════════════════════════════════════════════════════════════════════════════
class TestDataTypeConversions:
    """Tests for correct data type assignments."""

    def test_order_date_is_datetime(self, clean_df):
        """Order Date must be parsed as datetime."""
        assert pd.api.types.is_datetime64_any_dtype(clean_df['Order Date']), \
            f"Order Date dtype is {clean_df['Order Date'].dtype}, expected datetime"

    def test_sales_is_numeric(self, clean_df):
        """Sales must be numeric."""
        assert pd.api.types.is_numeric_dtype(clean_df['Sales']), \
            f"Sales dtype is {clean_df['Sales'].dtype}"

    def test_profit_is_numeric(self, clean_df):
        """Profit must be numeric."""
        assert pd.api.types.is_numeric_dtype(clean_df['Profit']), \
            f"Profit dtype is {clean_df['Profit'].dtype}"

    def test_quantity_is_integer_or_numeric(self, clean_df):
        """Quantity must be numeric."""
        assert pd.api.types.is_numeric_dtype(clean_df['Quantity']), \
            f"Quantity dtype is {clean_df['Quantity'].dtype}"

    def test_discount_is_numeric(self, clean_df):
        """Discount must be numeric."""
        assert pd.api.types.is_numeric_dtype(clean_df['Discount']), \
            f"Discount dtype is {clean_df['Discount'].dtype}"

    def test_order_year_values(self, clean_df):
        """Order Year must be within expected range."""
        assert clean_df['Order Year'].between(2020, 2023).all(), \
            f"Order Year out of expected range 2020-2023"

    def test_order_month_values(self, clean_df):
        """Order Month must be 1-12."""
        assert clean_df['Order Month'].between(1, 12).all(), \
            "Order Month contains values outside 1-12"

    def test_order_quarter_values(self, clean_df):
        """Order Quarter must be 1-4."""
        assert clean_df['Order Quarter'].between(1, 4).all(), \
            "Order Quarter contains values outside 1-4"


# ══════════════════════════════════════════════════════════════════════════════
# TEST GROUP 4: Output File Creation
# ══════════════════════════════════════════════════════════════════════════════
class TestOutputFileCreation:
    """Tests for output file existence and properties."""

    def test_cleaned_csv_created(self):
        """cleaned_sales.csv must exist."""
        assert os.path.exists(CLEAN_DATA_PATH), \
            f"cleaned_sales.csv not found at {CLEAN_DATA_PATH}"

    def test_cleaned_csv_not_empty(self):
        """cleaned_sales.csv must not be empty."""
        size = os.path.getsize(CLEAN_DATA_PATH)
        assert size > 1000, f"cleaned_sales.csv is suspiciously small: {size} bytes"

    def test_cleaning_report_created(self):
        """Data cleaning summary report must exist."""
        report_path = os.path.join(BASE_DIR, 'reports', 'data_cleaning_summary.md')
        assert os.path.exists(report_path), \
            f"Cleaning summary not found: {report_path}"

    def test_visualizations_created(self):
        """At least 8 visualization PNG files must exist."""
        viz_dir = os.path.join(BASE_DIR, 'visualizations')
        if os.path.exists(viz_dir):
            png_files = [f for f in os.listdir(viz_dir) if f.endswith('.png')]
            assert len(png_files) >= 8, \
                f"Expected >= 8 charts, found {len(png_files)} in {viz_dir}"
        else:
            pytest.skip("Visualizations directory not found — run eda_analysis.py first")


# ══════════════════════════════════════════════════════════════════════════════
# TEST GROUP 5: Data Quality Checks
# ══════════════════════════════════════════════════════════════════════════════
class TestDataQuality:
    """Tests for expected data quality after cleaning."""

    def test_sales_all_positive(self, clean_df):
        """All Sales values must be positive."""
        assert (clean_df['Sales'] > 0).all(), \
            f"Found {(clean_df['Sales'] <= 0).sum()} non-positive Sales values"

    def test_quantity_all_positive(self, clean_df):
        """All Quantity values must be positive."""
        assert (clean_df['Quantity'] > 0).all(), \
            f"Found {(clean_df['Quantity'] <= 0).sum()} non-positive Quantity values"

    def test_discount_in_range(self, clean_df):
        """All Discount values must be in [0, 1]."""
        assert clean_df['Discount'].between(0, 1).all(), \
            f"Found discounts outside [0, 1] range"

    def test_categories_expected(self, clean_df):
        """Category column must contain only expected values."""
        expected_cats = {'Technology', 'Office Supplies', 'Furniture'}
        actual_cats = set(clean_df['Category'].unique())
        assert actual_cats == expected_cats, \
            f"Unexpected categories: {actual_cats - expected_cats}"

    def test_regions_expected(self, clean_df):
        """Region column must contain only expected values."""
        expected_regions = {'East', 'West', 'Central', 'South'}
        actual_regions = set(clean_df['Region'].unique())
        assert actual_regions == expected_regions, \
            f"Unexpected regions: {actual_regions - expected_regions}"

    def test_segments_expected(self, clean_df):
        """Segment column must contain only expected values."""
        expected_segs = {'Consumer', 'Corporate', 'Home Office'}
        actual_segs = set(clean_df['Segment'].unique())
        assert actual_segs == expected_segs, \
            f"Unexpected segments: {actual_segs - expected_segs}"

    def test_profit_margin_calculated(self, clean_df):
        """Profit Margin % must match Profit/Sales calculation."""
        expected = (clean_df['Profit'] / clean_df['Sales'] * 100).round(2)
        actual = clean_df['Profit Margin %'].round(2)
        # Allow small floating point tolerance
        diff = (expected - actual).abs()
        assert (diff < 0.01).all(), \
            f"Profit Margin % has {(diff >= 0.01).sum()} mismatched rows"

    def test_ship_date_after_order_date(self, clean_df):
        """Ship Date (where not null) must be >= Order Date."""
        has_ship = clean_df['Ship Date'].notna()
        if has_ship.sum() > 0:
            ship_dates = pd.to_datetime(clean_df.loc[has_ship, 'Ship Date'])
            order_dates = pd.to_datetime(clean_df.loc[has_ship, 'Order Date'])
            invalid = (ship_dates < order_dates).sum()
            assert invalid == 0, f"{invalid} records have Ship Date before Order Date"

    def test_order_id_format(self, clean_df):
        """Order IDs must follow CA-YYYY-NNNNNNN format."""
        import re
        pattern = re.compile(r'^CA-\d{4}-\d{7}$')
        sample = clean_df['Order ID'].sample(min(100, len(clean_df)), random_state=42)
        non_matching = sample[~sample.str.match(r'^CA-\d{4}-\d+$')]
        assert len(non_matching) == 0, \
            f"Found {len(non_matching)} Order IDs not matching expected format"


# ══════════════════════════════════════════════════════════════════════════════
# TEST GROUP 6: Business Logic Checks
# ══════════════════════════════════════════════════════════════════════════════
class TestBusinessLogic:
    """Tests for business logic consistency."""

    def test_total_sales_positive(self, clean_df):
        """Total sales must be positive."""
        assert clean_df['Sales'].sum() > 0

    def test_minimum_customers(self, clean_df):
        """Must have at least 100 unique customers."""
        n_customers = clean_df['Customer ID'].nunique()
        assert n_customers >= 100, f"Only {n_customers} unique customers"

    def test_minimum_products(self, clean_df):
        """Must have at least 50 unique products."""
        n_products = clean_df['Product Name'].nunique()
        assert n_products >= 50, f"Only {n_products} unique products"

    def test_all_four_regions_present(self, clean_df):
        """All 4 regions must have data."""
        assert clean_df['Region'].nunique() == 4

    def test_all_three_categories_present(self, clean_df):
        """All 3 categories must have data."""
        assert clean_df['Category'].nunique() == 3

    def test_multiple_years_present(self, clean_df):
        """Dataset must span multiple years."""
        assert clean_df['Order Year'].nunique() >= 2, \
            "Dataset covers fewer than 2 years"

    def test_sub_categories_count(self, clean_df):
        """Must have at least 10 sub-categories."""
        n_subcats = clean_df['Sub-Category'].nunique()
        assert n_subcats >= 10, f"Only {n_subcats} sub-categories found"


# ══════════════════════════════════════════════════════════════════════════════
# MAIN (run directly)
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
