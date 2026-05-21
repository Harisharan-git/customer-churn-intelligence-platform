import random
import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password="YOUR_DB_PASSWORD"",
    database="customer_churn_system"
)

cursor = conn.cursor()

cursor.execute("SELECT customer_id FROM customers")
customer_ids = cursor.fetchall()

insert_query = """
INSERT INTO customer_usage (
    customer_id,
    usage_month,
    data_usage_gb,
    call_minutes,
    sms_count,
    streaming_hours,
    device_count
)
VALUES (%s,%s,%s,%s,%s,%s,%s)
"""

usage_data = []

months = [
    "2025-01-01","2025-02-01","2025-03-01","2025-04-01",
    "2025-05-01","2025-06-01","2025-07-01","2025-08-01",
    "2025-09-01","2025-10-01","2025-11-01","2025-12-01"
]

for customer in customer_ids:
    customer_id = customer[0]

    for month in months:
        usage_data.append((
            customer_id,
            month,
            round(random.uniform(5, 500), 2),
            random.randint(50, 3000),
            random.randint(10, 1000),
            round(random.uniform(1, 250), 2),
            random.randint(1, 6)
        ))

        if len(usage_data) >= 5000:
            cursor.executemany(insert_query, usage_data)
            conn.commit()
            usage_data = []
            print("Inserted batch...")

if usage_data:
    cursor.executemany(insert_query, usage_data)
    conn.commit()

cursor.close()
conn.close()

print("Customer usage data inserted successfully!")