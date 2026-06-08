# ==========================================
# LOAD MODEL AND PREDICT
# Household Energy Consumption Dataset
# ==========================================

import pandas as pd
import pickle

# ------------------------------------------
# Load Saved Model
# ------------------------------------------

with open("power_consumption_model.pkl", "rb") as file:
    model = pickle.load(file)

print("Model Loaded Successfully!")

# ------------------------------------------
# Predict for 3 Different Households
# ------------------------------------------

new_data = pd.DataFrame({

    'Global_reactive_power': [0.10, 0.25, 0.35],

    'Voltage': [239.5, 242.0, 236.8],

    'Global_intensity': [6.5, 10.2, 14.5],

    'Sub_metering_1': [0, 1, 2],

    'Sub_metering_2': [1, 0, 3],

    'Sub_metering_3': [17, 18, 20]
})

predictions = model.predict(new_data)

print("\nPredicted Power Consumption")

for i, value in enumerate(predictions, start=1):
    print(
        f"Household {i}:",
        round(value, 4),
        "kW"
    )