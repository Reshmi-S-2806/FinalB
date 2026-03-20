import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# 1️⃣ Load dataset
data = pd.read_csv("fraud_training_dataset.csv")

# 2️⃣ Features used in the model
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

X = data[feature_columns]
y = data["fraud"]

# 3️⃣ Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4️⃣ Train model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# 5️⃣ Test accuracy
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))

# 6️⃣ Save model
pickle.dump(model, open("fraud_model.pkl", "wb"))

print("Model saved as fraud_model.pkl")