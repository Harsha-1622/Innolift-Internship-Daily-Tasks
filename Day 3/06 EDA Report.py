# ==========================================
# FULL EDA REPORT
# Household Energy Consumption Dataset
# ==========================================

import os
import pandas as pd
import numpy as np

# ------------------------------------------
# EDA Function
# ------------------------------------------

def eda_report(df):

    print("\n========== FULL EDA REPORT ==========\n")

    # Shape
    print("1. Dataset Shape")
    print(df.shape)

    print("\n" + "="*50)

    # Column Names
    print("2. Column Names")
    print(df.columns.tolist())

    print("\n" + "="*50)

    # Data Types
    print("3. Data Types")
    print(df.dtypes)

    print("\n" + "="*50)

    # Missing Values
    print("4. Missing Values")
    print(df.isnull().sum())

    print("\n" + "="*50)

    # Numerical Summary
    print("5. Numerical Column Summary")

    numeric_cols = df.select_dtypes(include=np.number)

    print(numeric_cols.describe())

    print("\n" + "="*50)

    # Object Columns Value Counts
    print("6. Object Column Value Counts")

    object_cols = df.select_dtypes(include='object')

    if len(object_cols.columns) == 0:
        print("No Object Columns Found")

    else:
        for col in object_cols.columns:

            print(f"\nColumn: {col}")

            print(df[col].value_counts().head(10))

    print("\n" + "="*50)

    # Duplicate Rows
    print("7. Duplicate Rows")
    print(df.duplicated().sum())

    print("\n" + "="*50)

    # Unique Values
    print("8. Unique Values")
    print(df.nunique())

    print("\n========== REPORT COMPLETED ==========\n")


# ------------------------------------------
# Load Dataset
# ------------------------------------------

file_candidates = [
    "07 household_power_consumption.csv",
    "household_power_consumption.csv",
    "household_power_consumption"
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

# Rename Combined Column
df.rename(columns={'Date_Time': 'Datetime'}, inplace=True)

# Replace Missing Values Symbol
df.replace('?', np.nan, inplace=True)

# Convert Numeric Columns

columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity'
]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ------------------------------------------
# Run EDA Report
# ------------------------------------------

eda_report(df)