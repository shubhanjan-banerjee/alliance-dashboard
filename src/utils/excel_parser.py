# Excel parsing utilities for data ingestion

import pandas as pd
from db.database_operations import clean_date, clean_number

def parse_performance_data(sheet) -> (pd.DataFrame, list):
    """Parse and validate the 'Global Strategic Alliances Partner Performance Dashboard as of May 2025 [Sample data]' sheet."""
    errors = []
    df = pd.read_excel(sheet, sheet_name=0)
    # Standardize columns
    expected_cols = [
        'Associate Name', 'Alliance Type', 'Business Unit', 'Geo', 'Certification Name', 'Completion Date', 'Feedback'
    ]
    df = df.rename(columns={c: c.strip() for c in df.columns})
    for col in expected_cols:
        if col not in df.columns:
            errors.append(f"Missing column: {col}")
    # Clean and validate data
    for idx, row in df.iterrows():
        date_val = clean_date(row['Completion Date'])
        if not date_val:
            errors.append(f"Row {idx+2}: Invalid date format in 'Completion Date'")
        df.at[idx, 'Completion Date'] = date_val
    return df, errors

def parse_global_metrics(sheet) -> (pd.DataFrame, list):
    errors = []
    df = pd.read_excel(sheet, sheet_name='Global')
    # Example: parse and clean numeric columns
    for idx, row in df.iterrows():
        for col in ['Total', 'India', 'NA', 'GGM']:
            val = clean_number(row.get(col, None))
            if val is None:
                errors.append(f"Row {idx+2}: Invalid number in '{col}'")
            df.at[idx, col] = val
    return df, errors
