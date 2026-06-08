# ==========================================
# SAVE YOUR MODEL
# Household Energy Consumption Dataset
# ==========================================

import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

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
# Train Model
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

# ------------------------------------------
# Save Model
# ------------------------------------------

with open("power_consumption_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model Saved Successfully!")