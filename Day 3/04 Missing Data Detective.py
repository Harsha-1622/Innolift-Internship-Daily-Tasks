# ==========================================
# MISSING DATA DETECTIVE
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
# Replace '?' with NaN
# ------------------------------------------
df.replace('?', np.nan, inplace=True)

# ==========================================
# MISSING DATA DETECTIVE
# ==========================================

print("========== MISSING DATA DETECTIVE ==========\n")

# Total Missing Values
total_missing = df.isnull().sum().sum()

print("Total Missing Values:", total_missing)

print()

# Missing Values Per Column
print("Missing Values Per Column:")
print(df.isnull().sum())

print()

# Columns Having Missing Values
print("Columns with Missing Data:")

missing_columns = df.columns[df.isnull().any()]

for col in missing_columns:
    print(col)

print()

# Percentage of Missing Values
print("Missing Value Percentage:")

for col in df.columns:

    percentage = (
        df[col].isnull().sum()
        / len(df)
    ) * 100

    print(f"{col}: {percentage:.2f}%")

print()

# ==========================================
# CUSTOM FUNCTION
# ==========================================

def missing_count(column_name):
    """
    Returns missing value count
    for a specific column
    """
    return df[column_name].isnull().sum()

print("========== FUNCTION OUTPUT ==========\n")

print(
    "Missing Values in Global_active_power:",
    missing_count("Global_active_power")
)

print(
    "Missing Values in Voltage:",
    missing_count("Voltage")
)

print()

# ==========================================
# ROWS CONTAINING MISSING VALUES
# ==========================================

rows_with_missing = df[df.isnull().any(axis=1)]

print("Rows Containing Missing Values:")
print(len(rows_with_missing))

print()

# Display first 5 rows with missing values
print(rows_with_missing.head())

print()

# ==========================================
# HANDLE MISSING VALUES
# ==========================================

# Fill missing values with Forward Fill
df_filled = df.fillna(method='ffill')

print("Missing Values After Filling:")

print(df_filled.isnull().sum().sum())

print()

# Save cleaned dataset
df_filled.to_csv(
    "09 cleaned_household_power_consumption.csv",
    index=False
)

print("Cleaned dataset saved successfully!")

print()
print("Missing Data Detective Completed Successfully!")