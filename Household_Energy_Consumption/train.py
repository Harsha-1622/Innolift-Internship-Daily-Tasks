import pandas as pd
import numpy as np
import pickle

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

# Features
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

# Target
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

print("\n========== MODEL PERFORMANCE ==========")
print(f"RMSE: {rmse:.4f}")
print(f"R² Score: {r2:.4f}")
print(f"Accuracy: {r2 * 100:.2f}%")

# Save Model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("\nModel saved as model.pkl")
