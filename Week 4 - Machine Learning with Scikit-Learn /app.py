from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# 1. Load your model
with open("/Users/anaghabhole/Documents/Projects/DataScience-and-Quant-Portfolio/Week 4 - Machine Learning with Scikit-Learn /best_xgb.pkl", "rb") as f:
    best_xgb = pickle.load(f)

# 2. Define route for predictions


@app.route("/predict", methods=["GET"])
def predict_churn():
    """
    Expects JSON data in the format:
    {
       "gender": "Female",
       "tenure": 12,
       ...
    }
    Returns a JSON response with the prediction.
    """
    # 2A. Parse JSON from the incoming request
    # input_data = request.get_json()
    input_data = {
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "Yes",
        "tenure": 24,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "No",
        "DeviceProtection": "Yes",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "PaperlessBilling": "No",
        "MonthlyCharges": 60.50,
        "TotalCharges": 1452.00,
        "InternetService": "DSL",
        "Contract": "Month-to-month",
        "PaymentMethod": "Electronic check",
        "MonthlyChargePerTenure": 2.56
    }

    # 2B. Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # 2C. Preprocess (exactly as in training)
    # Convert 'TotalCharges' to numeric, coerce errors into NaN
    input_df["TotalCharges"] = pd.to_numeric(
        input_df["TotalCharges"], errors="coerce")

    # Drop rows with missing TotalCharges (small number of rows)
    input_df.dropna(subset=["TotalCharges"], inplace=True)

    input_df.dropna(inplace=True)
    input_df["TotalCharges"] = pd.to_numeric(
        input_df["TotalCharges"], errors="coerce")

    print(input_df.isna().sum().sum())  # Should be 0
    # Should also be 0
    print(input_df.replace([np.inf, -np.inf], np.nan).isna().sum().sum())

    # Example: Simple map for binary columns
    binary_cols = ["Partner", "Dependents", "PhoneService",
                   "MultipleLines", "OnlineSecurity", "OnlineBackup",
                   "DeviceProtection", "TechSupport", "StreamingTV",
                   "StreamingMovies", "PaperlessBilling"]

    for col in binary_cols:
        input_df[col] = input_df[col].map({"Yes": 1, "No": 0})

    # Example: One-Hot Encoding
    multi_cat_cols = ["InternetService", "Contract", "PaymentMethod"]
    input_df = pd.get_dummies(
        input_df, columns=multi_cat_cols, drop_first=True)

    # List of all possible categories for the categorical variables
    internet_services = ['Fiber optic', 'No']
    contracts = ['One year', 'Two year']
    payment_methods = ['Credit card (automatic)', 'Electronic check', 'Mailed check']

    # Add missing dummy variables to the input data and set their values to 0
    for service in internet_services:
        if 'InternetService_' + service not in input_df.columns:
            input_df['InternetService_' + service] = 0

    for contract in contracts:
        if 'Contract_' + contract not in input_df.columns:
            input_df['Contract_' + contract] = 0

    for method in payment_methods:
        if 'PaymentMethod_' + method not in input_df.columns:
            input_df['PaymentMethod_' + method] = 0

    print(input_df.columns)

    # Gender binary map
    input_df["gender"] = input_df["gender"].map({"Female": 1, "Male": 0})

    num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    input_df["tenure"] = pd.to_numeric(input_df["tenure"], errors="coerce")
    input_df["MonthlyCharges"] = pd.to_numeric(
        input_df["MonthlyCharges"], errors="coerce")

    scaler = StandardScaler()
    input_df[num_cols] = scaler.fit_transform(input_df[num_cols])

    input_df.dropna(inplace=True)

    input_df["MonthlyChargePerTenure"] = input_df["MonthlyCharges"] / \
        (input_df["tenure"] + 1)

    # 2D. Model prediction
    prediction = best_xgb.predict(input_df)[0]

    # 2E. Return a JSON response
    return jsonify({"prediction": int(prediction)})

# 3. Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
