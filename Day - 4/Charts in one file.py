# ==========================================
# CHARTS IN ONE FILE
# Household Energy Consumption Dataset
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

df.rename(columns={'Date_Time': 'Datetime'}, inplace=True)

# Replace missing values
df.replace('?', np.nan, inplace=True)

# Convert columns to numeric
columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity'
]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ------------------------------------------
# Create Month Column
# ------------------------------------------

df['Month'] = df['Datetime'].dt.month

# ==========================================
# 1. BAR CHART
# Average Power Consumption by Month
# ==========================================

monthly_power = df.groupby('Month')[
    'Global_active_power'
].mean()

plt.figure(figsize=(8,5))
monthly_power.plot(kind='bar')

plt.title("Average Power Consumption by Month")
plt.xlabel("Month")
plt.ylabel("Average Power")

plt.tight_layout()
plt.savefig("bar_chart.png")
plt.close()

# ==========================================
# 2. SCATTER PLOT
# Voltage vs Global Active Power
# ==========================================

plt.figure(figsize=(8,5))

plt.scatter(
    df['Voltage'],
    df['Global_active_power'],
    alpha=0.5
)

plt.title("Voltage vs Global Active Power")
plt.xlabel("Voltage")
plt.ylabel("Global Active Power")

plt.tight_layout()
plt.savefig("scatter_plot.png")
plt.close()

# ==========================================
# 3. HISTOGRAM
# Voltage Distribution
# ==========================================

plt.figure(figsize=(8,5))

plt.hist(
    df['Voltage'].dropna(),
    bins=30
)

plt.title("Voltage Distribution")
plt.xlabel("Voltage")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig("histogram.png")
plt.close()

# ==========================================
# 4. LINE CHART
# Average Trend
# ==========================================

avg_power = df['Global_active_power'].mean()
avg_reactive = df['Global_reactive_power'].mean()
avg_intensity = df['Global_intensity'].mean()

x = [
    "Active Power",
    "Reactive Power",
    "Intensity"
]

y = [
    avg_power,
    avg_reactive,
    avg_intensity
]

plt.figure(figsize=(8,5))

plt.plot(
    x,
    y,
    marker='o'
)

plt.title("Average Energy Trend")
plt.xlabel("Parameters")
plt.ylabel("Average Value")

plt.tight_layout()
plt.savefig("line_chart.png")
plt.close()

# ==========================================
# Completed
# ==========================================

print("All charts created successfully!")
print("Saved Files:")
print("1. bar_chart.png")
print("2. scatter_plot.png")
print("3. histogram.png")
print("4. line_chart.png")