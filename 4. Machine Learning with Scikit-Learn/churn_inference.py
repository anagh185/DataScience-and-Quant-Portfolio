import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load trained model (after saving with pickle/joblib)
with open("best_xgb.pkl", "rb") as f:
    best_xgb = pickle.load(f)

def predict_churn(input_data: dict):
    # Convert dict to DataFrame
    input_df = pd.DataFrame([input_data])
    # Preprocess data exactly as in training (scaling, encoding, etc.)
    # ... same transformations as training ...

    # Convert 'TotalCharges' to numeric, coerce errors into NaN
    input_df["TotalCharges"] = pd.to_numeric(input_df["TotalCharges"], errors="coerce")

    # Drop rows with missing TotalCharges (small number of rows)
    input_df.dropna(subset=["TotalCharges"], inplace=True)

    input_df.dropna(inplace=True)
    input_df["TotalCharges"] = pd.to_numeric(input_df["TotalCharges"], errors="coerce")


    print(input_df.isna().sum().sum())  # Should be 0
    print(input_df.replace([np.inf, -np.inf], np.nan).isna().sum().sum())  # Should also be 0

    # Example: Simple map for binary columns
    binary_cols = ["Partner", "Dependents", "PhoneService", 
               "MultipleLines", "OnlineSecurity", "OnlineBackup", 
               "DeviceProtection", "TechSupport", "StreamingTV", 
               "StreamingMovies", "PaperlessBilling", "Churn"]

    for col in binary_cols:
        input_df[col] = df[col].map({"Yes": 1, "No": 0})

    # Example: One-Hot Encoding
    multi_cat_cols = ["InternetService", "Contract", "PaymentMethod"]
    input_df = pd.get_dummies(input_df, columns=multi_cat_cols, drop_first=True)

    # Gender binary map
    input_df["gender"] = input_df["gender"].map({"Female": 1, "Male": 0})

    input_df.drop(["customerID"], axis=1, inplace=True)
    
    

    num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    input_df["tenure"] = pd.to_numeric(input_df["tenure"], errors="coerce")
    input_df["MonthlyCharges"] = pd.to_numeric(input_df["MonthlyCharges"], errors="coerce")

    scaler = StandardScaler()
    input_df[num_cols] = scaler.fit_transform(input_df[num_cols])
    
    input_df.dropna(inplace=True)

    input_df["MonthlyChargePerTenure"] = input_df["MonthlyCharges"] / (input_df["tenure"] + 1)

    X = input_df.drop(["Churn"], axis=1)
    y = input_df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    prediction = best_xgb.predict(input_df)

    return prediction[0]
