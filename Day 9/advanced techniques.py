# ==========================================
# ADVANCED TECHNIQUES
# Household Energy Consumption Forecaster
# ==========================================

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

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

print("Data Cleaning Completed!")

# ==========================================
# FEATURES
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

# ==========================================
# LOAD TUNED MODEL
# ==========================================

print("\nLoading tuned_model.pkl...\n")

model = joblib.load(
    "tuned_model.pkl"
)

print("Model Loaded Successfully!")

# ==========================================
# TASK 1
# FEATURE IMPORTANCE ANALYSIS
# ==========================================

print("\n========== TASK 1 ==========")
print("Feature Importance Analysis\n")

importances = model.feature_importances_

importance_df = pd.DataFrame({

    'Feature': X.columns,

    'Importance': importances

})

importance_df = importance_df.sort_values(
    by='Importance',
    ascending=False
)

print(importance_df)

# Plot

plt.figure(
    figsize=(12, 7)
)

bars = plt.barh(
    importance_df['Feature'],
    importance_df['Importance']
)

plt.gca().invert_yaxis()

plt.title(
    'Feature Importance Analysis',
    fontsize=16,
    fontweight='bold'
)

plt.xlabel(
    'Importance Score',
    fontsize=12
)

plt.ylabel(
    'Features',
    fontsize=12
)

# Add values on bars

for bar in bars:

    width = bar.get_width()

    plt.text(
        width + 0.0005,
        bar.get_y() + bar.get_height()/2,
        f"{width:.6f}",
        va='center'
    )

plt.grid(
    axis='x',
    linestyle='--',
    alpha=0.5
)

plt.tight_layout()

plt.savefig(
    'feature_importance.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()

print(
    "\nfeature_importance.png saved!"
)
# ==========================================
# TASK 2
# CLASS IMBALANCE CHECK
# ==========================================

print("\n========== TASK 2 ==========")

print(
    "\nClass imbalance and SMOTE are not applicable "
    "for regression projects."
)

print(
    "\nTarget Variable Statistics:\n"
)

print(
    df['Global_active_power'].describe()
)

# ==========================================
# TASK 3
# MODEL EXPLAINABILITY
# ==========================================

print("\n========== TASK 3 ==========")

def explain_prediction(
    model,
    feature_names
):

    importances = model.feature_importances_

    feature_scores = list(
        zip(
            feature_names,
            importances
        )
    )

    feature_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_3 = feature_scores[:3]

    print(
        "\nTop 3 Features Influencing Predictions:\n"
    )

    for i, (name, score) in enumerate(
        top_3,
        1
    ):

        print(
            f"{i}. {name} "
            f"(Importance: {score:.4f})"
        )

    return top_3

top_features = explain_prediction(
    model,
    X.columns
)
# ==========================================
# TASK 4
# OUTPUT ENRICHMENT
# ==========================================

print("\n========== TASK 4 ==========\n")

def enrich_power(prediction):

    prediction = float(
        round(
            prediction,
            3
        )
    )

    if prediction < 1:

        category = "Low Consumption"

        advice = (
            "Power usage is low."
        )

    elif prediction < 3:

        category = (
            "Moderate Consumption"
        )

        advice = (
            "Power usage is within "
            "normal range."
        )

    else:

        category = (
            "High Consumption"
        )

        advice = (
            "Power usage is high. "
            "Consider saving energy."
        )

    return {

        "Predicted Power":
        prediction,

        "Category":
        category,

        "Advice":
        advice
    }

# ------------------------------------------
# TEST OUTPUT ENRICHMENT
# ------------------------------------------

print(
    "Testing Output Enrichment:\n"
)

test_prediction = 2.5

test_result = enrich_power(
    test_prediction
)

print(
    test_result
)
# ==========================================
# TASK 5
# REAL WORLD TEST CASES
# ==========================================

print("\n========== TASK 5 ==========")

samples = [

{
    "Global_reactive_power":0.1,
    "Voltage":240,
    "Global_intensity":5,
    "Sub_metering_1":0,
    "Sub_metering_2":1,
    "Sub_metering_3":10
},

{
    "Global_reactive_power":0.2,
    "Voltage":235,
    "Global_intensity":10,
    "Sub_metering_1":2,
    "Sub_metering_2":1,
    "Sub_metering_3":20
},

{
    "Global_reactive_power":0.01,
    "Voltage":240,
    "Global_intensity":1,
    "Sub_metering_1":0,
    "Sub_metering_2":0,
    "Sub_metering_3":1
},

{
    "Global_reactive_power":0.4,
    "Voltage":225,
    "Global_intensity":20,
    "Sub_metering_1":7,
    "Sub_metering_2":5,
    "Sub_metering_3":40
},

{
    "Global_reactive_power":0.5,
    "Voltage":220,
    "Global_intensity":25,
    "Sub_metering_1":10,
    "Sub_metering_2":8,
    "Sub_metering_3":50
}

]

# Store results

results = []

for i, sample in enumerate(samples, 1):

    sample_df = pd.DataFrame([sample])

    prediction = model.predict(
        sample_df
    )[0]

    result = enrich_power(
        prediction
    )

    results.append({

        "Sample": i,

        "Predicted Power":
        result["Predicted Power"],

        "Category":
        result["Category"],

        "Advice":
        result["Advice"]

    })

# Convert to DataFrame

results_df = pd.DataFrame(
    results
)

print(
    "\n===== 5 SAMPLE PREDICTIONS =====\n"
)

print(
    results_df.to_string(
        index=False
    )
)

# Save Results

results_df.to_csv(
    "sample_predictions.csv",
    index=False
)

print(
    "\nsample_predictions.csv saved!"
)
# ==========================================
# FINAL SUMMARY
# ==========================================

print(
    "\n=================================="
)
print(
    "\nGenerated Files:"
)

print(
    "feature_importance.png"
)
print(
    "sample_predictions.csv"
)