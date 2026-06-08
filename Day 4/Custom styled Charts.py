# ==========================================
# CUSTOM STYLED CHART
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

# Convert column to numeric
df['Global_active_power'] = pd.to_numeric(
    df['Global_active_power'],
    errors='coerce'
)

# ------------------------------------------
# Create Month Column
# ------------------------------------------

df['Month'] = df['Datetime'].dt.month

# Average Power Consumption by Month
monthly_avg = df.groupby('Month')[
    'Global_active_power'
].mean()

# Overall Mean
overall_mean = monthly_avg.mean()

# ------------------------------------------
# Custom Colors
# ------------------------------------------

colors = [
    'red', 'blue', 'green', 'orange',
    'purple', 'cyan', 'gold', 'pink',
    'brown', 'gray', 'lime', 'teal'
]

# ------------------------------------------
# Create Chart
# ------------------------------------------

plt.figure(figsize=(12,6))

bars = plt.bar(
    monthly_avg.index,
    monthly_avg.values,
    color=colors,
    edgecolor='black',
    label='Monthly Average Power'
)

# Mean Line
plt.axhline(
    y=overall_mean,
    color='black',
    linestyle='--',
    linewidth=2,
    label=f'Overall Mean = {overall_mean:.2f}'
)

# Value Labels on Bars
for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f'{bar.get_height():.2f}',
        ha='center',
        va='bottom'
    )

# Titles and Labels
plt.title(
    "Average Household Power Consumption by Month",
    fontsize=16,
    fontweight='bold'
)

plt.xlabel("Month", fontsize=12)
plt.ylabel("Average Power Consumption", fontsize=12)

# Grid
plt.grid(
    axis='y',
    linestyle=':',
    alpha=0.7
)

# X-axis Labels
plt.xticks(
    monthly_avg.index,
    rotation=0
)

# Legend
plt.legend()

# Layout
plt.tight_layout()

# Show Chart
plt.show()

print("Custom Styled Chart Generated Successfully!")

