import pandas as pd
import joblib

# Load Final Tuned Model
model = joblib.load(
    "models/final_model.pkl"
)

def predict(inputs):

    try:

        # Input Validation
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
            model.predict(
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
# TEST CASES
# ==========================================

sample = {

    "Global_reactive_power": 0.1,

    "Voltage": 240,

    "Global_intensity": 5,

    "Sub_metering_1": 0,

    "Sub_metering_2": 1,

    "Sub_metering_3": 10
}

result = predict(sample)

print(result)
