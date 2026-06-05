# ==========================================
# CLEAN YOUR DATA
# Household Energy Consumption Forecaster
# ==========================================

import pandas as pd
import numpy as np

# ------------------------------------------
# Load Dataset
# ------------------------------------------

file_path = "household_power_consumption.csv"

df = pd.read_csv(
    file_path,
    sep=',',
    parse_dates=[['Date', 'Time']],
    low_memory=False
)

# Rename Combined Column
df.rename(columns={'Date_Time': 'Datetime'}, inplace=True)

print("Dataset Loaded Successfully!")
print()

# ------------------------------------------
# Replace '?' with NaN
# ------------------------------------------

df.replace('?', np.nan, inplace=True)

# ------------------------------------------
# Convert Columns to Numeric
# ------------------------------------------

numeric_columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3'
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ------------------------------------------
# Missing Values Before Cleaning
# ------------------------------------------

print("Missing Values Before Cleaning:")
print(df.isnull().sum())

print("\nTotal Missing Values:")
print(df.isnull().sum().sum())

# ------------------------------------------
# Fill Missing Values with Mean
# ------------------------------------------

for col in numeric_columns:
    df[col] = df[col].fillna(df[col].mean())

# ------------------------------------------
# Verify Missing Values After Cleaning
# ------------------------------------------

print("\n" + "="*50)

print("Missing Values After Cleaning:")
print(df.isnull().sum())

print("\nTotal Missing Values After Cleaning:")
print(df.isnull().sum().sum())

# ------------------------------------------
# Dataset Information
# ------------------------------------------

print("\nDataset Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nData Cleaning Completed Successfully!")
# ==========================================
# OBSERVATIONS
# ==========================================

# 1. Missing values were present in multiple
#    power consumption columns.

# 2. The '?' symbols were converted into NaN values.

# 3. All numerical missing values were replaced
#    using the mean of their respective columns.

# 4. After cleaning, the dataset contains
#    zero missing values.

# 5. The cleaned dataset is ready for machine
#    learning model training.