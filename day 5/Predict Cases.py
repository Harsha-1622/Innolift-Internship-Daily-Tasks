# ==========================================
# LOAD MODEL & PREDICT 3 CASES
# Household Energy Consumption Forecaster
# ==========================================

import pickle
import pandas as pd

# ------------------------------------------
# Load Saved Model
# ------------------------------------------

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

print("Model Loaded Successfully!\n")

# ------------------------------------------
# New Household Inputs
# ------------------------------------------

new_data = pd.DataFrame({

    'Global_reactive_power': [0.15, 0.25, 0.35],

    'Voltage': [239.8, 242.1, 236.5],

    'Global_intensity': [7.5, 10.2, 14.8],

    'Sub_metering_1': [0, 1, 2],

    'Sub_metering_2': [1, 0, 3],

    'Sub_metering_3': [17, 18, 20]

})

# ------------------------------------------
# Predict
# ------------------------------------------

predictions = model.predict(new_data)

# ------------------------------------------
# Display Results
# ------------------------------------------

print("========== PREDICTIONS ==========\n")

for i, prediction in enumerate(predictions, start=1):

    print(
        f"Household {i} Predicted Power Consumption: "
        f"{prediction:.4f} kW"
    )