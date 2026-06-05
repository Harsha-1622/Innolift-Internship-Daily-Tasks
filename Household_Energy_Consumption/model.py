import pandas as pd
import numpy as np
import pickle
import os

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load Dataset
df = pd.read_csv(
    "data/household_power_consumption.csv",
    low_memory=False
)

# Create Datetime Column
df['Datetime'] = pd.to_datetime(
    df['Date'] + ' ' + df['Time'],
    dayfirst=True
)

# Replace Missing Values
df.replace('?', np.nan, inplace=True)

# Numeric Columns
numeric_columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3'
]

# Convert to Numeric
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Fill Missing Values
for col in numeric_columns:
    df[col] = df[col].fillna(df[col].mean())

print("Dataset Loaded and Cleaned Successfully")

# Create Charts Folder
os.makedirs("charts", exist_ok=True)

# Histogram
plt.figure(figsize=(8,5))
plt.hist(df['Global_active_power'], bins=30, edgecolor='black')
plt.title("Distribution of Global Active Power")
plt.xlabel("Power")
plt.ylabel("Frequency")
plt.savefig("charts/histogram.png")
plt.close()

# Scatter Plot
plt.figure(figsize=(8,5))
plt.scatter(
    df['Global_intensity'],
    df['Global_active_power'],
    alpha=0.5
)
plt.title("Intensity vs Power")
plt.xlabel("Global Intensity")
plt.ylabel("Global Active Power")
plt.savefig("charts/scatter_plot.png")
plt.close()

# Heatmap
plt.figure(figsize=(10,6))
sns.heatmap(
    df[numeric_columns].corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.savefig("charts/correlation_heatmap.png")
plt.close()

print("Charts Generated Successfully")

# Features and Target
X = df[
    [
        'Global_reactive_power',
        'Voltage',
        'Global_intensity',
        'Sub_metering_1',
        'Sub_metering_2',
        'Sub_metering_3'
    ]
]

y = df['Global_active_power']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# Model
model = LinearRegression()

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Metrics
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n========== RESULTS ==========")
print(f"RMSE: {rmse:.4f}")
print(f"R² Score: {r2:.4f}")
print(f"Accuracy: {r2 * 100:.2f}%")

# Save Model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("\nModel saved as model.pkl")
