# ==========================================
# CSV EXPLORER 
# Household Energy Consumption Dataset
# ==========================================

import os
import pandas as pd
import numpy as np

# ------------------------------------------
# Load Dataset
# ------------------------------------------
file_candidates = [
    "07 household_power_consumption.csv"
]
file_path = next((f for f in file_candidates if os.path.exists(f)), None)

if file_path is None:
    raise FileNotFoundError(
        f"No dataset file found. Checked: {file_candidates}"
    )

df = pd.read_csv(
    file_path,
    sep=',',
    parse_dates=[['Date', 'Time']],
    low_memory=False
)

# Rename combined column
df.rename(columns={'Date_Time': 'Datetime'}, inplace=True)

print(f"Dataset Loaded Successfully from {file_path}")
print()

# ------------------------------------------
# Replace Missing Values
# ------------------------------------------
df.replace('?', np.nan, inplace=True)

# ------------------------------------------
# Convert Columns to Numeric
# ------------------------------------------
columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity'
]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ==========================================
# CSV EXPLORER
# ==========================================

print("========== CSV EXPLORER ==========\n")

print("Dataset Shape:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head())

print("\nLast 5 Records:")
print(df.tail())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# ==========================================
# COUNT OPERATIONS
# ==========================================

print("\n========== COUNT OPERATIONS ==========\n")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))
print("Total Cells:", df.size)

# ==========================================
# CUSTOM CONDITION FUNCTION
# ==========================================

def count_condition(column_name, condition):
    """
    Counts rows satisfying a condition
    """
    count = condition(df[column_name]).sum()
    return count

# Count Global Active Power > 5
power_gt5 = count_condition(
    'Global_active_power',
    lambda x: x > 5
)

# Count Voltage > 240
voltage_gt240 = count_condition(
    'Voltage',
    lambda x: x > 240
)

print("\n========== CONDITIONAL COUNTS ==========\n")

print("Power Consumption > 5 kW:", power_gt5)

print("Voltage > 240:", voltage_gt240)

# ==========================================
# UNIQUE VALUE COUNTS
# ==========================================

print("\n========== UNIQUE COUNTS ==========\n")

for col in ['Global_active_power', 'Voltage']:
    print(f"{col}:", df[col].nunique(), "unique values")

print("\nCSV Explorer Completed Successfully!")