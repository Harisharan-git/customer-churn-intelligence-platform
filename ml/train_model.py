import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load dataset
df = pd.read_csv("customer_churn_dataset.csv")

print("Dataset loaded")
print(df.shape)

# Drop unnecessary columns
drop_cols = [
    "customer_id",
    "customer_code",
    "first_name",
    "last_name",
    "join_date",
    "city",
    "state"
]

df.drop(columns=drop_cols, inplace=True, errors="ignore")

# Fill nulls
df.fillna("Unknown", inplace=True)

# Categorical columns
categorical_cols = [
    "gender",
    "contract_type",
    "internet_service",
    "payment_method"
]

# Encode safely
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].astype(str)
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])

# Convert remaining numeric columns
for col in df.columns:
    if col != "churn":
        df[col] = pd.to_numeric(df[col], errors="coerce")

df.fillna(0, inplace=True)

# Features / target
X = df.drop("churn", axis=1)
y = df["churn"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training model...")

# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Metrics
print("Accuracy:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "churn_model.pkl")

joblib.dump(model, MODEL_PATH)
print("Saved at:", MODEL_PATH)

print("Model saved successfully!")