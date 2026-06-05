# ==========================================
# DOWNLOAD & LOAD DATASET
# Household Energy Consumption Forecaster
# ==========================================

import pandas as pd

# Load Dataset
file_path = "household_power_consumption.csv"

df = pd.read_csv(
    file_path,
    sep=',',
    parse_dates=[['Date', 'Time']],
    low_memory=False
)

# Rename Combined Column
df.rename(columns={'Date_Time': 'Datetime'}, inplace=True)

# ==========================================
# DISPLAY DATASET INFORMATION
# ==========================================

print("Dataset Loaded Successfully!")
print()

# Shape of Dataset
print("Dataset Shape (Rows, Columns):")
print(df.shape)

print("\n" + "=" * 50)

# First 5 Records
print("First 5 Records:")
print(df.head())

print("\n" + "=" * 50)

# Data Types
print("Data Types:")
print(df.dtypes)

print("\n" + "=" * 50)

# Column Names
print("Column Names:")
print(df.columns.tolist())

print("\nDataset Loading Completed Successfully!")