# ==========================================
# GROUP & COMPARE
# Household Energy Consumption Dataset
# ==========================================
import os
import pandas as pd
import numpy as np

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

df.rename(columns={'Date_Time': 'Datetime'}, inplace=True)

print(f"Dataset Loaded Successfully from {file_path}")
print()

# ------------------------------------------
# Data Cleaning
# ------------------------------------------
df.replace('?', np.nan, inplace=True)

columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity'
]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ------------------------------------------
# Create Groups
# ------------------------------------------
df['Power_Category'] = np.where(
    df['Global_active_power'] > 5,
    'High',
    'Normal'
)

# ==========================================
# GROUP & COMPARE
# ==========================================

print("========== GROUP & COMPARE ==========\n")

# Function 1 - head()
print("1. First 5 Records")
print(df.head())

# Function 2 - tail()
print("\n2. Last 5 Records")
print(df.tail())

# Function 3 - shape
print("\n3. Dataset Shape")
print(df.shape)

# Function 4 - columns
print("\n4. Column Names")
print(df.columns.tolist())

# Function 5 - info()
print("\n5. Dataset Information")
print(df.info())

# Function 6 - describe()
print("\n6. Statistical Summary")
print(df.describe())

# Function 7 - groupby()
print("\n7. Average Power by Category")
print(
    df.groupby('Power_Category')
    ['Global_active_power']
    .mean()
)

# Function 8 - count()
print("\n8. Count by Category")
print(
    df.groupby('Power_Category')
    ['Global_active_power']
    .count()
)

# Function 9 - max()
print("\n9. Maximum Power by Category")
print(
    df.groupby('Power_Category')
    ['Global_active_power']
    .max()
)

# Function 10 - min()
print("\n10. Minimum Power by Category")
print(
    df.groupby('Power_Category')
    ['Global_active_power']
    .min()
)

# Function 11 - sum()
print("\n11. Total Power by Category")
print(
    df.groupby('Power_Category')
    ['Global_active_power']
    .sum()
)

# Function 12 - value_counts()
print("\n12. Category Counts")
print(df['Power_Category'].value_counts())

# Function 13 - sort_values()
print("\n13. Top 10 Highest Power Records")
print(
    df.sort_values(
        by='Global_active_power',
        ascending=False
    )
    [['Datetime', 'Global_active_power']]
    .head(10)
)

# Function 14 - nunique()
print("\n14. Unique Values Count")
print(df.nunique())

# Function 15 - isnull()
print("\n15. Missing Values")
print(df.isnull().sum())

# ==========================================
# CUSTOM COMPARISON FUNCTION
# ==========================================

def compare_groups(column):
    print(f"\nComparison of {column}")

    print(
        df.groupby('Power_Category')[column]
        .agg(['count', 'mean', 'min', 'max'])
    )

compare_groups('Voltage')
