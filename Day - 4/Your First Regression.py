# ==========================================
# YOUR FIRST REGRESSION
# Household Energy Consumption Dataset
# ==========================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove missing values
df.dropna(inplace=True)

# ------------------------------------------
# Features and Target
# ------------------------------------------

# All numeric columns except target
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

# Target column
y = df['Global_active_power']

# ------------------------------------------
# Train Test Split
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

# ------------------------------------------
# Predictions
# ------------------------------------------

predictions = model.predict(X_test)

# ------------------------------------------
# Evaluation
# ------------------------------------------

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(
    y_test,
    predictions
)

print("========== MODEL PERFORMANCE ==========")

print("RMSE :", round(rmse, 4))
print("R² Score :", round(r2, 4))

# ------------------------------------------
# Predict for New Household Data
# ------------------------------------------

new_household = pd.DataFrame({
    'Global_reactive_power': [0.20],
    'Voltage': [240.5],
    'Global_intensity': [8.5],
    'Sub_metering_1': [0],
    'Sub_metering_2': [1],
    'Sub_metering_3': [17]
})

prediction = model.predict(new_household)

print("\n========== NEW PREDICTION ==========")
print(
    "Predicted Global Active Power :",
    round(prediction[0], 4),
    "kW"
)