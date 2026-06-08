# ==========================================
# DATAFRAME BUILDER
# Household Energy Consumption Dataset
# ==========================================

# Import Library
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
    low_memory=False
)

if {'Date', 'Time'}.issubset(df.columns):
    df['Datetime'] = pd.to_datetime(
        df['Date'].astype(str) + ' ' + df['Time'].astype(str),
        dayfirst=True,
        errors='coerce'
    )
elif 'Date_Time' in df.columns:
    df['Datetime'] = pd.to_datetime(
        df['Date_Time'],
        dayfirst=True,
        errors='coerce'
    )
else:
    raise KeyError(
        "Dataset must contain 'Date' and 'Time' or 'Date_Time' columns."
    )

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
# DATAFRAME BUILDER OPERATIONS
# ==========================================

print("========== DATAFRAME BUILDER ==========\n")

# Shape of DataFrame
print("Dataset Shape:")
print(df.shape)

print()

# Column Names
print("Column Names:")
print(df.columns.tolist())

print()

# Data Types
print("Data Types:")
print(df.dtypes)

print()

# First 5 Rows
print("First 5 Records:")
print(df.head())

print()

# Last 5 Rows
print("Last 5 Records:")
print(df.tail())

print()

# Missing Values
print("Missing Values:")
print(df.isnull().sum())

print()

# Statistical Summary
print("Statistical Summary:")
print(df.describe())

print()

# ------------------------------------------
# Filtering Records
# ------------------------------------------

high_voltage = df[df['Voltage'] > 240]

print("Records with Voltage > 240:")
print(high_voltage[['Datetime', 'Voltage']].head())

print()

# ------------------------------------------
# Create New Column
# ------------------------------------------

df['Power_Category'] = np.where(
    df['Global_active_power'] > 5,
    'High',
    'Normal'
)

print("New Column Added Successfully")
print()

print(df[['Global_active_power', 'Power_Category']].head())

print()

# ------------------------------------------
# Value Counts
# ------------------------------------------

print("Power Category Counts:")
print(df['Power_Category'].value_counts())

print()

# ------------------------------------------
# Sorting Data
# ------------------------------------------

sorted_power = df.sort_values(
    by='Global_active_power',
    ascending=False
)

print("Top 10 Highest Power Consumption Records:")
print(
    sorted_power[
        ['Datetime', 'Global_active_power']
    ].head(10)
)

print()

# ------------------------------------------
# Save Updated DataFrame
# ------------------------------------------

df.to_csv(
    "08 updated_household_power_consumption.csv",
    index=False
)

print("Updated DataFrame saved successfully!")

print()
print("DataFrame Builder Completed Successfully")
