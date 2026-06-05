# ==========================================
# VISUALISE YOUR DATASET
# Household Energy Consumption Forecaster
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

# ------------------------------------------
# Data Cleaning
# ------------------------------------------

df.replace('?', np.nan, inplace=True)

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
    df[col] = pd.to_numeric(
        df[col],
        errors='coerce'
    )

# Fill missing values
for col in numeric_columns:
    df[col] = df[col].fillna(
        df[col].mean()
    )

# ==========================================
# CHART 1 - HISTOGRAM
# Distribution of Target Variable
# ==========================================

plt.figure(figsize=(8,5))

plt.hist(
    df['Global_active_power'],
    bins=30,
    edgecolor='black'
)

plt.title(
    "Distribution of Global Active Power"
)

plt.xlabel(
    "Global Active Power"
)

plt.ylabel(
    "Frequency"
)

plt.tight_layout()

plt.savefig(
    "histogram.png"
)

plt.close()

# ==========================================
# CHART 2 - SCATTER PLOT
# Top Feature vs Target
# ==========================================

plt.figure(figsize=(8,5))

plt.scatter(
    df['Global_intensity'],
    df['Global_active_power'],
    alpha=0.5
)

plt.title(
    "Global Intensity vs Global Active Power"
)

plt.xlabel(
    "Global Intensity"
)

plt.ylabel(
    "Global Active Power"
)

plt.tight_layout()

plt.savefig(
    "scatter_plot.png"
)

plt.close()

# ==========================================
# CHART 3 - CORRELATION HEATMAP
# ==========================================

plt.figure(figsize=(10,6))

sns.heatmap(
    df[numeric_columns].corr(),
    annot=True,
    cmap='coolwarm'
)

plt.title(
    "Correlation Heatmap"
)

plt.tight_layout()

plt.savefig(
    "correlation_heatmap.png"
)

plt.close()

# ==========================================
# Completed
# ==========================================

print("Charts Generated Successfully!")
print()

print("Saved Files:")
print("1. histogram.png")
print("2. scatter_plot.png")
print("3. correlation_heatmap.png")