import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("password="YOUR_DB_PASSWORD"")

engine = create_engine(
    f"mysql+mysqlconnector://root:{password}@127.0.0.1/customer_churn_system"
)

print("Connecting to database...")

customers = pd.read_sql("SELECT * FROM customers", engine)
print("Customers loaded")

usage = pd.read_sql("SELECT * FROM customer_usage", engine)
print("Usage loaded")

billing = pd.read_sql("SELECT * FROM billing", engine)
print("Billing loaded")

tickets = pd.read_sql("SELECT * FROM support_tickets", engine)
print("Tickets loaded")

usage_agg = usage.groupby("customer_id").agg({
    "data_usage_gb": "mean",
    "call_minutes": "mean",
    "sms_count": "mean",
    "streaming_hours": "mean",
    "device_count": "mean"
}).reset_index()

billing_agg = billing.groupby("customer_id").agg({
    "monthly_charge": "mean",
    "tax_amount": "mean",
    "discount": "mean",
    "payment_delay_days": "mean",
    "late_fee": "mean"
}).reset_index()

ticket_agg = tickets.groupby("customer_id").agg({
    "ticket_id": "count",
    "satisfaction_score": "mean"
}).reset_index()

ticket_agg.rename(columns={
    "ticket_id": "ticket_count"
}, inplace=True)

print("Merging data...")

df = customers.merge(usage_agg, on="customer_id", how="left")
df = df.merge(billing_agg, on="customer_id", how="left")
df = df.merge(ticket_agg, on="customer_id", how="left")

df["ticket_count"] = df["ticket_count"].fillna(0)
df["satisfaction_score"] = df["satisfaction_score"].fillna(5)

df.to_csv("customer_churn_dataset.csv", index=False)

print("Dataset created successfully!")
print(df.shape)