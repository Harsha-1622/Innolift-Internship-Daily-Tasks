# Household Energy Consumption Forecaster - IOT

## Project Overview

The Household Energy Consumption Forecaster is a Machine Learning project that predicts household electricity consumption using historical energy usage data. The project analyzes electrical parameters such as voltage, reactive power, current intensity, and sub-metering values to estimate future power consumption.

The goal of this project is to help users understand energy usage patterns, optimize electricity consumption, and improve energy efficiency.

---

## Problem Statement

Household electricity consumption varies depending on appliance usage and electrical conditions. Predicting energy consumption can help users monitor their usage, reduce electricity bills, and make informed decisions about energy management.

This project aims to build a Machine Learning model that predicts Global Active Power Consumption based on various electrical measurements.

---

## Dataset Source

**Dataset Name:** Household Power Consumption Dataset

**Source:** Kaggle

The dataset contains household electrical measurements collected over time, including power consumption, voltage, current intensity, and sub-metering information.

---

## Features Used (X)

The following features were used as input variables:

- Global_reactive_power
- Voltage
- Global_intensity
- Sub_metering_1
- Sub_metering_2
- Sub_metering_3

---

## Target Variable (Y)

- Global_active_power

The model predicts the household's Global Active Power Consumption.

---

## Data Preprocessing

The following preprocessing steps were performed:

- Loaded dataset using Pandas
- Combined Date and Time columns
- Replaced '?' values with NaN
- Converted numerical columns to appropriate data types
- Filled missing values using column mean
- Verified dataset quality before training

---

## Exploratory Data Analysis (EDA)

EDA was performed to understand the dataset and identify useful patterns.

### Analysis Performed

- Dataset Shape Analysis
- Missing Value Analysis
- Statistical Summary
- Feature Correlation Analysis
- Distribution Analysis

### Visualizations Created

1. Histogram of Global Active Power
2. Scatter Plot of Global Intensity vs Global Active Power
3. Correlation Heatmap

**Algorithm Used:** Gradient Boosting Regressor

Gradient Boosting Regressor was selected because it is an ensemble learning algorithm that combines multiple weak decision tree models to create a strong predictive model. It is well-suited for capturing complex and non-linear relationships in household energy consumption data, resulting in higher prediction accuracy than traditional regression methods.

---

## Model Evaluation

The model was evaluated using:

### RMSE (Root Mean Squared Error)

Measures the average prediction error between actual and predicted energy consumption values.

### R² Score

Measures how well the model explains the variation in energy consumption data.

### Accuracy Achieved

Accuracy (%) = R² Score × 100

* RMSE: 0.0418
* R² Score: 0.9989
* Accuracy: 99.89%

---

### Why Gradient Boosting Regressor?

* Handles complex and non-linear relationships effectively.
* Improves prediction accuracy by sequentially correcting previous errors.
* Produced the highest R² Score among the evaluated models.
* Achieved lower prediction error compared to the baseline model.
* Selected as the final model for the Household Energy Consumption Forecaster project.

## Project Structure

Household_Energy_Consumption_Forecaster/

│
├── household_power_consumption.csv
├── model.py
├── predict.py
├── model.pkl
├── visualize.py
├── requirements.txt
├── README.md
│
├── histogram.png
├── scatter_plot.png
└── correlation_heatmap.png

---

## How to Run the Project

### Step 1: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 2: Train the Model

```bash
python model.py
```

This will:
- Load the dataset
- Clean the data
- Train the Linear Regression model
- Evaluate performance
- Save model.pkl

### Step 3: Predict New Cases

```bash
python predict.py
```

This will:
- Load the saved model
- Predict power consumption for 3 new household cases

### Step 4: Generate Visualizations

```bash
python visualize.py
```

This will generate:

- histogram.png
- scatter_plot.png
- correlation_heatmap.png

---

## Real-World Applications

- Smart Home Energy Management
- Electricity Bill Forecasting
- Energy Consumption Monitoring
- IoT-Based Energy Analytics
- Energy Usage Optimization
- Sustainable Energy Planning

---

## Conclusion

This project demonstrates how Machine Learning can be used to forecast household electricity consumption based on historical electrical measurements. The developed model helps analyze energy usage patterns and provides predictions that can support smarter energy management decisions.
