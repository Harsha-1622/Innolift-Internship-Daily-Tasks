# ==========================================
# IMPORTS
# ==========================================
import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt


from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    GridSearchCV,
    RandomizedSearchCV
)

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)
# ==========================================
# CREATE FOLDERS
# ==========================================

os.makedirs("models", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# ==========================================
# LOAD DATASET
# ==========================================

print("Loading Dataset...\n")

df = pd.read_csv(
    "household_power_consumption.csv",
    low_memory=False
)

print("Original Dataset Shape:")
print(df.shape)

# ==========================================
# DATA CLEANING
# ==========================================

df.replace(
    '?',
    np.nan,
    inplace=True
)

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

df = df.sample(
    n=50000,
    random_state=42
)

print(
    "\nData Cleaning Completed!"
)

print(
    "Dataset Shape:",
    df.shape
)
# ==========================================
# FEATURE SELECTION
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

y = df[
    'Global_active_power'
]

print(
    "\nFeature Selection Completed!"
)

print(
    "Features Shape:",
    X.shape
)

print(
    "Target Shape:",
    y.shape
)

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42
)

print(
    "\nTrain-Test Split Completed!"
)

print(
    "X_train:",
    X_train.shape
)

print(
    "X_test :",
    X_test.shape
)

print(
    "y_train:",
    y_train.shape
)

print(
    "y_test :",
    y_test.shape
)
# ==========================================
# BASELINE MODEL
# ==========================================

print(
    "\nTraining Random Forest Baseline Model..."
)

baseline_model = RandomForestRegressor(

    n_estimators=100,

    random_state=42,

    n_jobs=-1
)

baseline_model.fit(

    X_train,

    y_train
)

print(
    "Baseline Model Trained!"
)

# ==========================================
# BASELINE EVALUATION
# ==========================================

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

print(
    "\n========== BASELINE MODEL ==========\n"
)

print(
    "RMSE :",
    round(baseline_rmse, 4)
)

print(
    "MAE  :",
    round(baseline_mae, 4)
)

print(
    "R²   :",
    round(baseline_r2, 4)
)
# ==========================================
# GRADIENT BOOSTING REGRESSOR
# ==========================================

print(
    "\nTraining Gradient Boosting Regressor..."
)

gbr_model = GradientBoostingRegressor(

    random_state=42
)

gbr_model.fit(

    X_train,

    y_train
)

print(
    "Gradient Boosting Model Trained!"
)

# ==========================================
# CROSS VALIDATION
# ==========================================

print(
    "\nRunning Cross Validation..."
)

cv_scores = cross_val_score(

    gbr_model,

    X_train,

    y_train,

    cv=5,

    scoring='neg_mean_squared_error'
)

cv_rmse = np.sqrt(

    -cv_scores
)

print(
    "\n========== CROSS VALIDATION ==========\n"
)

print(
    "Mean RMSE:",
    round(
        cv_rmse.mean(),
        4
    )
)

print(
    "Standard Deviation:",
    round(
        cv_rmse.std(),
        4
    )
)
# ==========================================
# HYPERPARAMETER TUNING
# ==========================================

print(
    "\nStarting Grid Search..."
)

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

print(
    "\n========== GRID SEARCH RESULTS ==========\n"
)

print(
    "Best Parameters:"
)

print(
    grid.best_params_
)

print(
    "\nBest Score:"
)

print(
    grid.best_score_
)
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
    "Cross Validation Error (MSE)"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "charts/validation_curve.png"
)

plt.show()

print(
    "\nvalidation_curve.png saved!"
)
# ==========================================
# RANDOMIZED SEARCH CV
# ==========================================

print(
    "\nStarting RandomizedSearchCV..."
)

random_search = RandomizedSearchCV(

    estimator=
    GradientBoostingRegressor(
        random_state=42
    ),

    param_distributions=
    param_grid,

    n_iter=10,

    cv=5,

    scoring=
    'neg_mean_squared_error',

    random_state=42,

    n_jobs=-1
)

random_search.fit(

    X_train,

    y_train
)

print(
    "\n========== RANDOMIZED SEARCH RESULTS ==========\n"
)

print(
    "Best Parameters:"
)

print(
    random_search.best_params_
)

print(
    "\nBest Score:"
)

print(
    random_search.best_score_
)
# ==========================================
# SELECT BEST MODEL
# ==========================================

grid_rmse = np.sqrt(
    -grid.best_score_
)

random_rmse = np.sqrt(
    -random_search.best_score_
)

if grid_rmse <= random_rmse:

    tuned_model = grid.best_estimator_

    best_method = "GridSearchCV"

else:

    tuned_model = random_search.best_estimator_

    best_method = "RandomizedSearchCV"

print(
    "\nBest Search Method:",
    best_method
)

# ==========================================
# TUNED MODEL EVALUATION
# ==========================================

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

print(
    "\n========== TUNED MODEL ==========\n"
)

print(
    "RMSE :",
    round(tuned_rmse, 4)
)

print(
    "MAE  :",
    round(tuned_mae, 4)
)

print(
    "R²   :",
    round(tuned_r2, 4)
)

# ==========================================
# COMPARISON TABLE
# ==========================================

comparison = pd.DataFrame({

    "Model": [

        "Random Forest",

        "Gradient Boosting"
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

print(
    "\n========== COMPARISON TABLE ==========\n"
)

print(
    comparison
)

comparison.to_csv(

    "comparison.csv",

    index=False
)

print(
    "\ncomparison.csv saved!"
)

# ==========================================
# ACTUAL VS PREDICTED PLOT
# ==========================================

plt.figure(
    figsize=(8, 6)
)

plt.scatter(

    y_test,

    tuned_predictions,

    alpha=0.5,

    color='blue'
)

plt.plot(

    [y_test.min(), y_test.max()],

    [y_test.min(), y_test.max()],

    color='red',

    linestyle='--',

    linewidth=2,

    label='Perfect Prediction'
)

plt.title(
    "Actual vs Predicted Values"
)

plt.xlabel(
    "Actual Values"
)

plt.ylabel(
    "Predicted Values"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "charts/actual_vs_predicted.png"
)

plt.show()
# ==========================================
# RESIDUAL PLOT
# ==========================================

residuals = y_test - tuned_predictions

plt.figure(
    figsize=(8, 6)
)

plt.scatter(

    tuned_predictions,

    residuals,

    alpha=0.5
)

plt.axhline(

    y=0,

    color='red',

    linestyle='--',

    linewidth=2
)

plt.title(
    "Residual Plot"
)

plt.xlabel(
    "Predicted Values"
)

plt.ylabel(
    "Residuals (Actual - Predicted)"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "charts/residual_plot.png"
)

plt.show()

print(
    "\nresidual_plot.png saved!"
)
# ==========================================
# FEATURE IMPORTANCE PLOT
# ==========================================

importance_df = pd.DataFrame({

    "Feature": X.columns,

    "Importance": tuned_model.feature_importances_
})

importance_df = importance_df.sort_values(

    by="Importance",

    ascending=False
)

print(
    "\n========== FEATURE IMPORTANCE ==========\n"
)

print(importance_df)

plt.figure(
    figsize=(12, 7)
)

bars = plt.barh(

    importance_df["Feature"],

    importance_df["Importance"]
)

plt.title(
    "Feature Importance Analysis",
    fontsize=16,
    fontweight='bold'
)

plt.xlabel(
    "Importance Score",
    fontsize=12
)

plt.ylabel(
    "Features",
    fontsize=12
)

plt.grid(
    axis='x',
    linestyle='--',
    alpha=0.5
)

plt.gca().invert_yaxis()

for bar in bars:

    width = bar.get_width()

    plt.text(

        width,

        bar.get_y() + bar.get_height()/2,

        f"{width:.6f}",

        va='center',

        ha='left',

        fontsize=11
    )

plt.tight_layout()

plt.savefig(
    "charts/feature_importance.png",
    dpi=300,
    bbox_inches='tight'
)

plt.show()

print(
    "\nfeature_importance.png saved!"
)
# ==========================================
# SAVE FINAL MODEL
# ==========================================

joblib.dump(

    tuned_model,

    "models/final_model.pkl"
)

print(
    "\nfinal_model.pkl saved!"
)
# ==========================================
# PREDICT FUNCTION
# ==========================================

def predict(inputs):

    try:

        if (
            inputs["Voltage"] <= 0
            or inputs["Global_intensity"] < 0
            or inputs["Global_reactive_power"] < 0
        ):

            return {

                "prediction": "ERROR",

                "category": "Invalid Input",

                "advice": "Invalid input values"
            }

        input_df = pd.DataFrame(
            [inputs]
        )

        prediction = float(
            tuned_model.predict(
                input_df
            )[0]
        )

        if prediction < 1:

            category = "Low Consumption"

            advice = "Power usage is low."

        elif prediction < 3:

            category = "Moderate Consumption"

            advice = (
                "Power usage is within normal range."
            )

        else:

            category = "High Consumption"

            advice = (
                "Power usage is high. Consider saving energy."
            )

        return {

            "prediction":
            round(prediction, 3),

            "category":
            category,

            "advice":
            advice
        }

    except Exception as e:

        return {

            "prediction": "ERROR",

            "category": "Exception",

            "advice": str(e)
        }

# ==========================================
# 10 TEST CASES
# ==========================================

def enrich_power(prediction):

    if prediction < 1:

        category = "Low Consumption"

        advice = "Power usage is low."

    elif prediction < 3:

        category = "Moderate Consumption"

        advice = "Power usage is within normal range."

    else:

        category = "High Consumption"

        advice = (
            "Power usage is high. Consider saving energy."
        )

    return category, advice


test_cases = [

{
    "Global_reactive_power":0.01,
    "Voltage":240,
    "Global_intensity":1,
    "Sub_metering_1":0,
    "Sub_metering_2":0,
    "Sub_metering_3":1
},

{
    "Global_reactive_power":0.05,
    "Voltage":238,
    "Global_intensity":3,
    "Sub_metering_1":0,
    "Sub_metering_2":1,
    "Sub_metering_3":5
},

{
    "Global_reactive_power":0.10,
    "Voltage":240,
    "Global_intensity":5,
    "Sub_metering_1":0,
    "Sub_metering_2":1,
    "Sub_metering_3":10
},

{
    "Global_reactive_power":0.15,
    "Voltage":236,
    "Global_intensity":8,
    "Sub_metering_1":1,
    "Sub_metering_2":2,
    "Sub_metering_3":15
},

{
    "Global_reactive_power":0.20,
    "Voltage":235,
    "Global_intensity":10,
    "Sub_metering_1":2,
    "Sub_metering_2":1,
    "Sub_metering_3":20
},

{
    "Global_reactive_power":0.25,
    "Voltage":232,
    "Global_intensity":12,
    "Sub_metering_1":3,
    "Sub_metering_2":2,
    "Sub_metering_3":25
},

{
    "Global_reactive_power":0.30,
    "Voltage":230,
    "Global_intensity":15,
    "Sub_metering_1":4,
    "Sub_metering_2":3,
    "Sub_metering_3":30
},

{
    "Global_reactive_power":0.40,
    "Voltage":225,
    "Global_intensity":20,
    "Sub_metering_1":7,
    "Sub_metering_2":5,
    "Sub_metering_3":40
},

{
    "Global_reactive_power":0.45,
    "Voltage":223,
    "Global_intensity":22,
    "Sub_metering_1":8,
    "Sub_metering_2":6,
    "Sub_metering_3":45
},

# Invalid test case
{
    "Global_reactive_power":-1,
    "Voltage":0,
    "Global_intensity":-5,
    "Sub_metering_1":-2,
    "Sub_metering_2":-1,
    "Sub_metering_3":-10
}

]

results = []

print(
    "\n========== 10 TEST CASES ==========\n"
)

for i, sample in enumerate(
    test_cases,
    start=1
):

    result = predict(
        sample
    )

    results.append({

        "Sample": i,

        "Predicted Power":
        result["prediction"],

        "Category":
        result["category"],

        "Advice":
        result["advice"]
    })
results_df = pd.DataFrame(
    results
)

print(
    results_df.to_string(
        index=False
    )
)

results_df.to_csv(

    "test_cases_results.csv",

    index=False
)

print(
    "\ntest_cases_results.csv saved!"
)
# ==========================================
# FINAL RESULT
# ==========================================

print(
    "\n========== FINAL RESULT ==========\n"
)

print(
    "Best Model : Gradient Boosting Regressor"
)

print(
    "RMSE :",
    round(tuned_rmse, 4)
)

print(
    "MAE :",
    round(tuned_mae, 4)
)

print(
    "R² Score :",
    round(tuned_r2, 4)
)