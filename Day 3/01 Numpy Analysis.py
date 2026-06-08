# ==========================================
# HOUSEHOLD ENERGY CONSUMPTION NUMPY ANALYZER
# ==========================================

# Import Libraries
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

# ------------------------------------------
# Analyze Global Active Power
# ------------------------------------------
power = df['Global_active_power'].dropna().to_numpy()

print("========== NUMPY ANALYZER ==========")

# Total Records
print("Total Records :", power.size)

# Sum
print("Total Power Consumption :", np.sum(power))

# Mean
print("Average Power Consumption :", np.mean(power))

# Median
print("Median Power Consumption :", np.median(power))

# Maximum
print("Maximum Power Consumption :", np.max(power))

# Minimum
print("Minimum Power Consumption :", np.min(power))

# Standard Deviation
print("Standard Deviation :", np.std(power))

# Variance
print("Variance :", np.var(power))

print()

# ------------------------------------------
# Conditional Counting
# ------------------------------------------

# Count power > 5
count_gt5 = np.sum(power > 5)

# Count power between 2 and 4
count_2_4 = np.sum((power >= 2) & (power <= 4))

# Count power < 1
count_lt1 = np.sum(power < 1)

# Count power > average
count_avg = np.sum(power > np.mean(power))

print("========== CONDITIONAL COUNTS ==========")

print("Power > 5 kW :", count_gt5)

print("Power Between 2 and 4 kW :", count_2_4)

print("Power < 1 kW :", count_lt1)

print("Power Greater Than Average :", count_avg)

print()

# ------------------------------------------
# Voltage Analysis
# ------------------------------------------
voltage = df['Voltage'].dropna().to_numpy()

print("========== VOLTAGE ANALYSIS ==========")

print("Average Voltage :", np.mean(voltage))

print("Maximum Voltage :", np.max(voltage))

print("Minimum Voltage :", np.min(voltage))

print("Voltage > 240 :", np.sum(voltage > 240))

print()

# ------------------------------------------
# Top 10 Highest Power Values
# ------------------------------------------
print("========== TOP 10 POWER VALUES ==========")

top10 = np.sort(power)[-10:]

print(top10)

print()

# ------------------------------------------
# Bottom 10 Lowest Power Values
# ------------------------------------------
print("========== LOWEST 10 POWER VALUES ==========")

bottom10 = np.sort(power)[:10]

print(bottom10)

print()

# ------------------------------------------
# Percentage of High Consumption Records
# ------------------------------------------
high_usage = np.sum(power > 5)

percentage = (high_usage / power.size) * 100

print("Percentage of High Consumption Records (>5 kW):")

print(round(percentage, 2), "%")

print()

print("Analysis Completed Successfully")