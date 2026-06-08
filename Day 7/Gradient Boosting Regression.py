import pandas as pd
import numpy as np
import joblib

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

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
print(df.shape)
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

print("Cleaning Completed!")

print(df.isnull().sum())
df = df.sample(
    n=50000,
    random_state=42
)

print("Reduced Dataset Shape:")
print(df.shape)
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

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print(X_train.shape)
print(X_test.shape)
rf_model = RandomForestRegressor(
    n_estimators=20,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(
    X_train,
    y_train
)

rf_pred = rf_model.predict(
    X_test
)

rf_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        rf_pred
    )
)

rf_mae = mean_absolute_error(
    y_test,
    rf_pred
)

rf_r2 = r2_score(
    y_test,
    rf_pred
)

print("Random Forest Completed!")
gb_model = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    random_state=42
)

gb_model.fit(
    X_train,
    y_train
)

gb_pred = gb_model.predict(
    X_test
)

gb_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        gb_pred
    )
)

gb_mae = mean_absolute_error(
    y_test,
    gb_pred
)

gb_r2 = r2_score(
    y_test,
    gb_pred
)

print("Gradient Boosting Completed!")
comparison = pd.DataFrame({

    "Model": [
        "Random Forest",
        "Gradient Boosting"
    ],

    "RMSE": [
        rf_rmse,
        gb_rmse
    ],

    "MAE": [
        rf_mae,
        gb_mae
    ],

    "R2 Score": [
        rf_r2,
        gb_r2
    ]
})

print(comparison)

comparison.to_csv(
    "comparison.csv",
    index=False
)

print("\ncomparison.csv saved!")
plt.figure(figsize=(8,5))

plt.scatter(
    y_test,
    gb_pred,
    alpha=0.5
)

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    'r--',
    linewidth=2
)

plt.title("Actual vs Predicted - Gradient Boosting")
plt.xlabel("Actual Power Consumption")
plt.ylabel("Predicted Power Consumption")

plt.savefig(
    "residual_plot.png"
)

plt.show()
if gb_r2 > rf_r2:

    best_model = gb_model
    best_name = "Gradient Boosting Regressor"
    best_score = gb_r2

else:

    best_model = rf_model
    best_name = "Random Forest Regressor"
    best_score = rf_r2

joblib.dump(
    best_model,
    "best_model.pkl"
)

print("========== FINAL RESULT ==========\n")

print("Best Model :", best_name)

print(
    "Best R² Score :",
    round(best_score, 4)
)

print("\nbest_model.pkl saved!")