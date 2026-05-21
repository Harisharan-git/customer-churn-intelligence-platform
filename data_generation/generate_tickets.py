import random
import mysql.connector
from datetime import datetime, timedelta

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
INSERT INTO support_tickets (
    customer_id,
    issue_type,
    priority,
    created_at,
    resolved_at,
    satisfaction_score
)
VALUES (%s,%s,%s,%s,%s,%s)
"""

issue_types = [
    "Network Issue",
    "Billing Complaint",
    "Slow Internet",
    "Service Downtime",
    "SIM Activation",
    "Payment Failure",
    "Account Issue"
]

priorities = ["Low", "Medium", "High"]

ticket_data = []

for customer in customer_ids:
    customer_id = customer[0]

    num_tickets = random.randint(0, 8)

    for _ in range(num_tickets):
        created = datetime.now() - timedelta(days=random.randint(1, 365))
        resolution_hours = random.randint(1, 72)
        resolved = created + timedelta(hours=resolution_hours)

        ticket_data.append((
            customer_id,
            random.choice(issue_types),
            random.choice(priorities),
            created,
            resolved,
            random.randint(1, 5)
        ))

        if len(ticket_data) >= 5000:
            cursor.executemany(insert_query, ticket_data)
            conn.commit()
            ticket_data = []
            print("Inserted ticket batch...")

if ticket_data:
    cursor.executemany(insert_query, ticket_data)
    conn.commit()

cursor.close()
conn.close()

print("Support ticket data inserted successfully!")