# ==========================================
# DAY 8 - HYPERPARAMETER TUNING
# Household Energy Consumption Forecaster
# ==========================================

import pandas as pd
import numpy as np
import joblib

import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    GridSearchCV
)

from sklearn.ensemble import GradientBoostingRegressor

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

# ==========================================
# LOAD DATASET
# ==========================================

print("Loading Dataset...\n")

df = pd.read_csv(
    "household_power_consumption.csv",
    low_memory=False
)

# ==========================================
# DATA CLEANING
# ==========================================

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

print("Data Cleaning Completed!")

# ==========================================
# REDUCE DATASET SIZE
# ==========================================

df = df.sample(
    n=50000,
    random_state=42
)

print("Dataset Shape:", df.shape)

# ==========================================
# FEATURES & TARGET
# ==========================================

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

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTrain-Test Split Completed!")

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)

# ==========================================
# BASELINE MODEL
# ==========================================

print("\nLoading best_model.pkl...")

baseline_model = joblib.load(
    "best_model.pkl"
)

baseline_predictions = baseline_model.predict(
    X_test
)

baseline_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        baseline_predictions
    )
)

baseline_mae = mean_absolute_error(
    y_test,
    baseline_predictions
)

baseline_r2 = r2_score(
    y_test,
    baseline_predictions
)

print("\n========== BASELINE MODEL ==========\n")

print("RMSE :", round(baseline_rmse, 4))
print("MAE  :", round(baseline_mae, 4))
print("R²   :", round(baseline_r2, 4))

# ==========================================
# CROSS VALIDATION
# ==========================================

print("\nRunning Cross Validation...")

cv_scores = cross_val_score(
    baseline_model,
    X_train,
    y_train,
    cv=5,
    scoring='neg_mean_squared_error'
)

cv_rmse = np.sqrt(-cv_scores)

print("\n========== CROSS VALIDATION ==========\n")

print(
    "Mean RMSE:",
    round(cv_rmse.mean(), 4)
)

print(
    "Standard Deviation:",
    round(cv_rmse.std(), 4)
)

# ==========================================
# PARAMETER GRID
# ==========================================

param_grid = {

    'n_estimators': [
        50,
        100,
        150
    ],

    'max_depth': [
        3,
        5,
        7
    ],

    'min_samples_split': [
        2,
        5,
        10
    ]
}

print("\nParameter Grid Created!")

# ==========================================
# GRID SEARCH
# ==========================================

print("\nStarting Grid Search...")

grid = GridSearchCV(

    estimator=
    GradientBoostingRegressor(
        random_state=42
    ),

    param_grid=
    param_grid,

    cv=5,

    scoring=
    'neg_mean_squared_error',

    n_jobs=-1
)

grid.fit(
    X_train,
    y_train
)

print("\n========== BEST PARAMETERS ==========\n")

print(
    grid.best_params_
)

print(
    "\nBest Score:",
    grid.best_score_
)

# ==========================================
# TUNED MODEL
# ==========================================

tuned_model = grid.best_estimator_

tuned_predictions = tuned_model.predict(
    X_test
)

tuned_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        tuned_predictions
    )
)

tuned_mae = mean_absolute_error(
    y_test,
    tuned_predictions
)

tuned_r2 = r2_score(
    y_test,
    tuned_predictions
)

# ==========================================
# COMPARISON TABLE
# ==========================================

comparison = pd.DataFrame({

    "Model": [
        "Baseline Model",
        "Tuned Model"
    ],

    "RMSE": [
        baseline_rmse,
        tuned_rmse
    ],

    "MAE": [
        baseline_mae,
        tuned_mae
    ],

    "R2 Score": [
        baseline_r2,
        tuned_r2
    ]
})

print("\n========== COMPARISON ==========\n")

print(comparison)

comparison.to_csv(
    "comparison.csv",
    index=False
)

print("\ncomparison.csv saved!")

# ==========================================
# VALIDATION CURVE
# ==========================================

results = pd.DataFrame(
    grid.cv_results_
)

plt.figure(
    figsize=(8, 5)
)

plt.plot(

    results[
        'param_n_estimators'
    ],

    -results[
        'mean_test_score'
    ],

    marker='o'
)

plt.title(
    "Validation Curve"
)

plt.xlabel(
    "Number of Estimators"
)

plt.ylabel(
    "Cross Validation Error"
)

plt.grid(True)

plt.savefig(
    "validation_curve.png"
)

plt.show()

# ==========================================
# SAVE TUNED MODEL
# ==========================================

joblib.dump(
    tuned_model,
    "tuned_model.pkl"
)

print("\nTuned Model Saved!")

# ==========================================
# FINAL RESULT
# ==========================================

print("\n========== FINAL RESULT ==========\n")

if tuned_rmse < baseline_rmse:

    print(
        "Tuned Model is Better!"
    )

else:

    print(
        "Baseline Model is Better!"
    )

print(
    "\nBaseline RMSE:",
    round(baseline_rmse, 4)
)

print(
    "Tuned RMSE:",
    round(tuned_rmse, 4)
)

print(
    "\nBest Parameters:"
)

print(
    grid.best_params_
)

print(
    "\nFiles Generated:"
)

print("comparison.csv")
print("validation_curve.png")
print("tuned_model.pkl")
