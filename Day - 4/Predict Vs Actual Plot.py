# ==========================================
# PREDICT VS ACTUAL PLOT
# Household Energy Consumption Dataset
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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

# ------------------------------------------
# Convert Columns to Numeric
# ------------------------------------------

columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity',
    'Sub_metering_1',
    'Sub_metering_2',
    'Sub_metering_3'
]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove missing values
df.dropna(inplace=True)

# ------------------------------------------
# Features and Target
# ------------------------------------------

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

# ------------------------------------------
# Train-Test Split
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ------------------------------------------
# Train Model
# ------------------------------------------

model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# ------------------------------------------
# Model Score
# ------------------------------------------

r2 = r2_score(y_test, y_pred)

print("R² Score:", round(r2, 4))

# ------------------------------------------
# Predict vs Actual Plot
# ------------------------------------------

plt.figure(figsize=(8,6))

# Scatter plot
plt.scatter(
    y_test,
    y_pred,
    alpha=0.5,
    label="Predicted vs Actual"
)

# Perfect Prediction Line
min_val = min(y_test.min(), y_pred.min())
max_val = max(y_test.max(), y_pred.max())

plt.plot(
    [min_val, max_val],
    [min_val, max_val],
    color='red',
    linewidth=2,
    label='Perfect Prediction'
)

plt.title("Actual vs Predicted Power Consumption")
plt.xlabel("Actual Global Active Power")
plt.ylabel("Predicted Global Active Power")

plt.legend()
plt.grid(True)

plt.show()

print("\nInterpretation:")
print("If most points lie close to the red diagonal line,")
print("the model predictions are accurate.")
print("Points far from the line indicate prediction errors.")