## Model Summary Card

### Project

Household Energy Consumption Forecaster - IOT

### Algorithm

Gradient Boosting Regressor (tuned using GridSearchCV and RandomizedSearchCV)

### Dataset

Household Power Consumption Dataset · 50,000 sampled records · 6 features

### Final Performance

| Metric                              |  Score |
| ----------------------------------- | -----: |
| RMSE                                | 0.0345 |
| MAE                                 | 0.0195 |
| R² Score                            | 0.9991 |
| Cross-Validation Mean RMSE          | 0.0352 |
| Cross-Validation Standard Deviation | 0.0013 |

### Best Hyperparameters

| Parameter         | Value |
| ----------------- | ----: |
| n_estimators      |   150 |
| max_depth         |     5 |
| min_samples_split |    10 |

### Input Features (in this exact order)

| Column                | Type  | Example Value |
| --------------------- | ----- | ------------: |
| Global_reactive_power | float |          0.10 |
| Voltage               | float |         240.0 |
| Global_intensity      | float |           5.0 |
| Sub_metering_1        | float |           0.0 |
| Sub_metering_2        | float |           1.0 |
| Sub_metering_3        | float |          10.0 |

### Target Variable

Global_active_power

### Required .pkl Files

| File            | Contents                          |
| --------------- | --------------------------------- |
| final_model.pkl | Tuned Gradient Boosting Regressor |

### Sample Input

```python
{
    "Global_reactive_power": 0.10,
    "Voltage": 240,
    "Global_intensity": 5,
    "Sub_metering_1": 0,
    "Sub_metering_2": 1,
    "Sub_metering_3": 10
}
```

### Sample Output

```python
{
    "prediction": 1.163,
    "category": "Moderate Consumption",
    "advice": "Power usage is within normal range."
}
```

### Generated Files

```text
comparison.csv
test_cases_results.csv

charts/
├── actual_vs_predicted.png
├── residual_plot.png
├── feature_importance.png
└── validation_curve.png

models/
└── final_model.pkl
```

### How to Use

```python
result = predict(input_dictionary)

print(result)
```

### Notes

* The model predicts household active power consumption.
* Predictions are categorized as Low, Moderate, or High Consumption.
* Invalid inputs are handled gracefully through input validation.
* Hyperparameter tuning was performed using both GridSearchCV and RandomizedSearchCV with 5-fold cross-validation.
