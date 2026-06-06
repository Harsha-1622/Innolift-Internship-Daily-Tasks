import pandas as pd
import numpy as np
import joblib

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)
file_path = "household_power_consumption.csv"

df = pd.read_csv(
    file_path,
    low_memory=False
)

print("Dataset Loaded Successfully!")
df['Datetime'] = pd.to_datetime(
    df['Date'] + ' ' + df['Time'],
    dayfirst=True
)

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

for col in numeric_columns:
    df[col] = df[col].fillna(
        df[col].mean()
    )

# Faster Training
df = df.sample(
    n=50000,
    random_state=42
)

print("Cleaning Completed!")
print("New Shape:", df.shape)
print("Shape:")
print(df.shape)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())
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

print("Features and Target Created!")
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)

print("y_train:", y_train.shape)
print("y_test :", y_test.shape)
from sklearn.preprocessing import StandardScaler
import joblib

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)

joblib.dump(
    scaler,
    "scaler.pkl"
)

print("Scaler Saved Successfully!")
plt.figure(figsize=(10,6))

sns.heatmap(
    df[numeric_columns].corr(),
    annot=True,
    cmap='coolwarm'
)

plt.title("Correlation Heatmap")

plt.show()
model = RandomForestRegressor(
    n_estimators=20,
    random_state=42,
    n_jobs=-1
)

print("Model Created!")
print("Training Started...")

model.fit(
    X_train_scaled,
    y_train
)

print("Model Trained Successfully!")
predictions = model.predict(
    X_test_scaled
)

print("Predictions Generated!")
rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)

mape = np.mean(
    np.abs(
        (y_test - predictions) / y_test
    )
) * 100

# Accuracy (for regression projects)
accuracy = r2 * 100

print("========== MODEL PERFORMANCE ==========\n")

print(f"RMSE     : {rmse:.4f}")
print(f"MAE      : {mae:.4f}")
print(f"R² Score : {r2:.4f}")
print(f"MAPE     : {mape:.2f}%")
print(f"Accuracy : {accuracy:.2f}%")

# ------------------------------------------
# ACTUAL VS PREDICTED GRAPH
# ------------------------------------------

plt.figure(figsize=(8,5))

plt.scatter(
    y_test,
    predictions,
    alpha=0.5
)

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    'r--',
    linewidth=2
)

plt.title("Actual vs Predicted Power Consumption")
plt.xlabel("Actual Power Consumption")
plt.ylabel("Predicted Power Consumption")

plt.grid(True)

plt.show()
print("========== FIRST 10 PREDICTIONS ==========\n")

for i in range(10):

    print(
        f"Actual: {y_test.iloc[i]:.4f}"
        f" | Predicted: {predictions[i]:.4f}"
    )

joblib.dump(
    model,
    "first_model.pkl"
)

print("\nModel Saved Successfully!")
print("File Created: first_model.pkl")