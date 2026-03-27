from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)

# Load trained ML model
with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

# Expected feature columns
feature_columns = [
    "amount",
    "hour_of_day",
    "day_of_week",
    "payment_method",
    "avg_transaction_amount",
    "transaction_amount_deviation",
    "transactions_last_10min",
    "transactions_last_1hour",
    "transactions_today",
    "merchant_risk_score",
    "first_time_merchant",
    "new_device",
    "device_type",
    "location_distance",
    "card_not_present",
    "international_transaction"
]


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        processed_data = {
            "amount": float(data.get("amount") or 0),
            "hour_of_day": int(data.get("hour_of_day") or 0),
            "day_of_week": int(data.get("day_of_week") or 0),
            "payment_method": int(data.get("payment_method") or 0),

            "avg_transaction_amount": float(data.get("avg_transaction_amount") or 0),
            "transaction_amount_deviation": float(data.get("transaction_amount_deviation") or 0),

            "transactions_last_10min": int(data.get("transactions_last_10min") or 0),
            "transactions_last_1hour": int(data.get("transactions_last_1hour") or 0),
            "transactions_today": int(data.get("transactions_today") or 0),

            "merchant_risk_score": int(data.get("merchant_risk_score") or 5),
            "first_time_merchant": int(data.get("first_time_merchant") or 0),

            "new_device": int(data.get("new_device") or 0),
            "device_type": int(data.get("device_type") or 0),

            "location_distance": float(data.get("location_distance") or 0),

            "card_not_present": int(data.get("card_not_present") or 1),
            "international_transaction": int(data.get("international_transaction") or 0)
        }

        fraud_reason = "Normal transaction"

        # Rule 1
        if processed_data["amount"] > 10000 and processed_data["new_device"] == 1:
            fraud_reason = "High amount transaction from new device"

        # Rule 2
        elif processed_data["location_distance"] > 1000:
            fraud_reason = "Transaction from unusual location"

        # Rule 3
        elif processed_data["transactions_last_10min"] >= 5:
            fraud_reason = "Multiple transactions in short time"

        # Convert to DataFrame
        df = pd.DataFrame([processed_data])
        df = df[feature_columns]

        # Predict fraud probability
        fraud_probability = model.predict_proba(df)[0][1]

        fraud_prediction = 1 if fraud_probability > 0.7 else 0

        if fraud_prediction == 1 and fraud_reason == "Normal transaction":
            fraud_reason = "Machine learning model detected suspicious pattern"

        return jsonify({
            "fraud_prediction": fraud_prediction,
            "fraud_score": float(fraud_probability),
            "fraud_reason": fraud_reason
        })

    except Exception as e:
        print("Prediction Error:", str(e))
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
