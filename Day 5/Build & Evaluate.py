# ==========================================
# BUILD & EVALUATE MODEL
# Household Energy Consumption Forecaster
# ==========================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_squared_error,
    r2_score
)

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

# Fill missing values with mean
for col in numeric_columns:
    df[col] = df[col].fillna(
        df[col].mean()
    )

# ------------------------------------------
# Define X and y
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
# Train-Test Split (80/20)
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("Training Records :", len(X_train))
print("Testing Records  :", len(X_test))

# ------------------------------------------
# Train Model
# ------------------------------------------

model = LinearRegression()

model.fit(
    X_train,
    y_train
)

# ------------------------------------------
# Predictions
# ------------------------------------------

predictions = model.predict(X_test)

# ------------------------------------------
# Evaluation
# ------------------------------------------

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

r2 = r2_score(
    y_test,
    predictions
)

print("\n========== MODEL PERFORMANCE ==========")

print("RMSE Score :", round(rmse, 4))

print("R² Score   :", round(r2, 4))

print(
    "\nModel Accuracy (%):",
    round(r2 * 100, 2)
)

# ------------------------------------------
# Interpretation
# ------------------------------------------

if r2 >= 0.70:
    print(
        "\nSuccess! Model achieved more than 70% accuracy."
    )
else:
    print(
        "\nModel accuracy is below 70%. Consider feature engineering."
    )
# ------------------------------------------
# Save Model
# ------------------------------------------

import pickle

with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel Saved Successfully as model.pkl")