from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# 1. Load your model
with open("/DataScience-and-Quant-Portfolio/Week 4 - Machine Learning with Scikit-Learn /best_xgb.pkl", "rb") as f:
    best_xgb = pickle.load(f)

# 2. Define route for predictions
@app.route("/predict", methods=["POST"])
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
    input_data = request.get_json()

    # 2B. Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # 2C. Preprocess (exactly as in training)
    # Example placeholders:
    if "TotalCharges" in input_df.columns:
        input_df["TotalCharges"] = pd.to_numeric(input_df["TotalCharges"], errors="coerce")

    yes_no_cols = ["Partner", "Dependents", "PhoneService", "OnlineSecurity"]
    for col in yes_no_cols:
        if col in input_df.columns:
            input_df[col] = input_df[col].map({"Yes": 1, "No": 0})

    # 2D. Model prediction
    prediction = best_xgb.predict(input_df)[0]

    # 2E. Return a JSON response
    return jsonify({"prediction": int(prediction)})

# 3. Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
