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
INSERT INTO billing (
    customer_id,
    billing_month,
    monthly_charge,
    tax_amount,
    discount,
    payment_delay_days,
    late_fee,
    payment_status
)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
"""

billing_data = []

months = [
    "2025-01-01","2025-02-01","2025-03-01","2025-04-01",
    "2025-05-01","2025-06-01","2025-07-01","2025-08-01",
    "2025-09-01","2025-10-01","2025-11-01","2025-12-01"
]

for customer in customer_ids:
    customer_id = customer[0]

    for month in months:
        monthly_charge = round(random.uniform(299, 2499), 2)
        tax_amount = round(monthly_charge * 0.18, 2)
        discount = round(random.uniform(0, 300), 2)
        payment_delay_days = random.randint(0, 20)
        late_fee = round(payment_delay_days * 10, 2)

        if payment_delay_days == 0:
            payment_status = "Paid"
        elif payment_delay_days <= 7:
            payment_status = "Late"
        else:
            payment_status = "Pending"

        billing_data.append((
            customer_id,
            month,
            monthly_charge,
            tax_amount,
            discount,
            payment_delay_days,
            late_fee,
            payment_status
        ))

        if len(billing_data) >= 5000:
            cursor.executemany(insert_query, billing_data)
            conn.commit()
            billing_data = []
            print("Inserted billing batch...")

if billing_data:
    cursor.executemany(insert_query, billing_data)
    conn.commit()

cursor.close()
conn.close()

print("Billing data inserted successfully!")