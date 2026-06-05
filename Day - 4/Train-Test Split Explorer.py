# ==========================================
# TRAIN-TEST SPLIT EXPLORER
# Household Energy Consumption Dataset
# ==========================================

import pandas as pd
import numpy as np

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

# Convert columns to numeric
columns = [
    'Global_active_power',
    'Global_reactive_power',
    'Voltage',
    'Global_intensity'
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
        'Voltage',
        'Global_reactive_power',
        'Global_intensity'
    ]
]

y = df['Global_active_power']

# ------------------------------------------
# Different Train-Test Splits
# ------------------------------------------

test_sizes = [0.1, 0.2, 0.3]

best_score = 0
best_split = 0

for size in test_sizes:

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=size,
        random_state=42
    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    score = r2_score(y_test, predictions)

    print("=" * 50)
    print(f"Test Size: {size}")
    print("Train Size:", len(X_train))
    print("Test Size :", len(X_test))
    print("R² Score  :", round(score, 4))

    if score > best_score:
        best_score = score
        best_split = size

# ------------------------------------------
# Best Split
# ------------------------------------------

print("\n" + "=" * 50)
print("BEST MODEL PERFORMANCE")
print("Best Test Size :", best_split)
print("Best R² Score  :", round(best_score, 4))
