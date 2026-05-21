import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Customer Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

.metric-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    transition: 0.3s;
}

.metric-card:hover {
    transform: scale(1.03);
}

.metric-title {
    font-size: 16px;
    color: #cbd5e1;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: white;
}

h1, h2, h3 {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "churn_model.pkl")

model = joblib.load(MODEL_PATH)

# ---------------- DATABASE ----------------
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="your_mysql_password",
    database="customer_churn_system"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    customers = pd.read_sql("SELECT * FROM customers", conn)
    billing = pd.read_sql("SELECT * FROM billing", conn)
    tickets = pd.read_sql("SELECT * FROM support_tickets", conn)
    usage = pd.read_sql("SELECT * FROM customer_usage", conn)
    return customers, billing, tickets, usage

customers, billing, tickets, usage = load_data()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    selected = option_menu(
        "Customer Intelligence",
        [
            "Executive Dashboard",
            "Customer 360",
            "Live Prediction",
            "What-If Simulator",
            "Customer Segmentation",
            "Anomaly Detection",
            "High Risk Watchlist"
        ],
        icons=[
            "bar-chart",
            "person-circle",
            "activity",
            "sliders",
            "diagram-3",
            "exclamation-triangle",
            "shield-exclamation"
        ],
        menu_icon="cast",
        default_index=0
    )

# ---------------- EXECUTIVE DASHBOARD ----------------
if selected == "Executive Dashboard":

    st.title("🚀 Executive Command Center")

    total_customers = len(customers)
    churn_customers = customers["churn"].sum()
    churn_rate = round((churn_customers / total_customers) * 100, 2)

    avg_revenue = round(billing["monthly_charge"].mean(), 2)
    avg_satisfaction = round(tickets["satisfaction_score"].mean(), 2)

    high_risk = billing[billing["payment_delay_days"] > 10]["customer_id"].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Customers</div>
            <div class="metric-value">{total_customers}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Churn Rate</div>
            <div class="metric-value">{churn_rate}%</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Revenue</div>
            <div class="metric-value">₹{avg_revenue}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Satisfaction</div>
            <div class="metric-value">{avg_satisfaction}</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">High Risk</div>
            <div class="metric-value">{high_risk}</div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        contract_fig = px.pie(
            customers,
            names="contract_type",
            title="Contract Distribution"
        )
        st.plotly_chart(contract_fig, use_container_width=True)

    with col2:
        payment_counts = customers["payment_method"].value_counts().reset_index()
        payment_counts.columns = ["payment_method", "count"]

        payment_fig = px.bar(
            payment_counts,
            x="payment_method",
            y="count",
            title="Payment Method Distribution"
        )
        st.plotly_chart(payment_fig, use_container_width=True)

    revenue_trend = billing.groupby("billing_month")["monthly_charge"].sum().reset_index()

    revenue_fig = px.line(
        revenue_trend,
        x="billing_month",
        y="monthly_charge",
        title="Revenue Trend"
    )

    st.plotly_chart(revenue_fig, use_container_width=True)

    # ---------------- CUSTOMER 360 ----------------
elif selected == "Customer 360":

    st.title("👤 Customer 360 Intelligence")

    customer_id = st.number_input(
        "Enter Customer ID",
        min_value=1,
        step=1
    )

    profile = customers[customers["customer_id"] == customer_id]

    if not profile.empty:

        st.subheader("Customer Profile")
        st.dataframe(profile, use_container_width=True)

        tab1, tab2, tab3 = st.tabs([
            "Usage History",
            "Billing History",
            "Support Tickets"
        ])

        with tab1:
            usage_data = usage[usage["customer_id"] == customer_id]

            if not usage_data.empty:
                usage_fig = px.line(
                    usage_data,
                    x="usage_month",
                    y="data_usage_gb",
                    title="Data Usage Trend"
                )
                st.plotly_chart(usage_fig, use_container_width=True)
                st.dataframe(usage_data, use_container_width=True)

        with tab2:
            billing_data = billing[billing["customer_id"] == customer_id]

            if not billing_data.empty:
                bill_fig = px.line(
                    billing_data,
                    x="billing_month",
                    y="monthly_charge",
                    title="Billing Trend"
                )
                st.plotly_chart(bill_fig, use_container_width=True)
                st.dataframe(billing_data, use_container_width=True)

        with tab3:
            ticket_data = tickets[tickets["customer_id"] == customer_id]

            if not ticket_data.empty:
                st.dataframe(ticket_data, use_container_width=True)

    else:
        st.warning("Customer not found.")

# ---------------- LIVE PREDICTION ----------------
elif selected == "Live Prediction":

    st.title("⚡ Live Prediction Studio")

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.slider("Age", 18, 75, 30)
        contract_type = st.selectbox(
            "Contract Type",
            ["Monthly", "Quarterly", "Yearly"]
        )
        internet_service = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber", "5G", "None"]
        )
        payment_method = st.selectbox(
            "Payment Method",
            ["Credit Card", "Debit Card", "UPI", "Net Banking"]
        )

    with col2:
        data_usage = st.slider("Data Usage (GB)", 0.0, 500.0, 100.0)
        call_minutes = st.slider("Call Minutes", 0, 5000, 500)
        sms_count = st.slider("SMS Count", 0, 2000, 100)
        streaming_hours = st.slider("Streaming Hours", 0.0, 500.0, 50.0)
        device_count = st.slider("Device Count", 1, 10, 2)

    st.subheader("Billing & Support")

    c1, c2, c3 = st.columns(3)

    with c1:
        monthly_charge = st.slider("Monthly Charge", 100.0, 5000.0, 1000.0)

    with c2:
        payment_delay = st.slider("Payment Delay Days", 0, 30, 2)

    with c3:
        ticket_count = st.slider("Support Tickets", 0, 20, 1)

    satisfaction = st.slider("Satisfaction Score", 1, 5, 4)

    if st.button("Predict Churn"):

        input_data = pd.DataFrame([{
            "gender": 1 if gender == "Male" else 0,
            "age": age,
            "contract_type": {
                "Monthly": 0,
                "Quarterly": 1,
                "Yearly": 2
            }[contract_type],
            "internet_service": {
                "DSL": 0,
                "Fiber": 1,
                "5G": 2,
                "None": 3
            }[internet_service],
            "payment_method": {
                "Credit Card": 0,
                "Debit Card": 1,
                "UPI": 2,
                "Net Banking": 3
            }[payment_method],
            "data_usage_gb": data_usage,
            "call_minutes": call_minutes,
            "sms_count": sms_count,
            "streaming_hours": streaming_hours,
            "device_count": device_count,
            "monthly_charge": monthly_charge,
            "tax_amount": monthly_charge * 0.18,
            "discount": 50,
            "payment_delay_days": payment_delay,
            "late_fee": payment_delay * 10,
            "ticket_count": ticket_count,
            "satisfaction_score": satisfaction
        }])

        probability = model.predict_proba(input_data)[0][1]

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            title={"text": "Churn Risk %"}
        ))

        st.plotly_chart(gauge, use_container_width=True)

        if probability > 0.75:
            st.error("🔥 HIGH RISK — Offer discount + support callback")

        elif probability > 0.40:
            st.warning("⚠️ MEDIUM RISK — Monitor closely")

        else:
            st.success("✅ LOW RISK — Stable customer")

# ---------------- WHAT IF SIMULATOR ----------------
elif selected == "What-If Simulator":

    st.title("🧠 What-If Business Simulator")

    st.write("Change customer behavior and see churn impact instantly.")

    payment_delay = st.slider("Payment Delay", 0, 30, 10)
    ticket_count = st.slider("Support Complaints", 0, 20, 5)
    monthly_charge = st.slider("Monthly Charge", 100.0, 5000.0, 1200.0)
    satisfaction = st.slider("Satisfaction", 1, 5, 3)

    sim_data = pd.DataFrame([{
        "gender": 1,
        "age": 35,
        "contract_type": 0,
        "internet_service": 1,
        "payment_method": 0,
        "data_usage_gb": 120,
        "call_minutes": 600,
        "sms_count": 100,
        "streaming_hours": 60,
        "device_count": 2,
        "monthly_charge": monthly_charge,
        "tax_amount": monthly_charge * 0.18,
        "discount": 50,
        "payment_delay_days": payment_delay,
        "late_fee": payment_delay * 10,
        "ticket_count": ticket_count,
        "satisfaction_score": satisfaction
    }])

    sim_prob = model.predict_proba(sim_data)[0][1]

    st.progress(int(sim_prob * 100))
    st.metric("Predicted Churn Risk", f"{round(sim_prob * 100, 2)}%")

    # ---------------- CUSTOMER SEGMENTATION ----------------
elif selected == "Customer Segmentation":

    st.title("🧩 Customer Segmentation Intelligence")

    merged = customers.merge(
        billing.groupby("customer_id")["monthly_charge"].mean().reset_index(),
        on="customer_id",
        how="left"
    )

    merged = merged.merge(
        usage.groupby("customer_id")["data_usage_gb"].mean().reset_index(),
        on="customer_id",
        how="left"
    )

    merged["monthly_charge"] = merged["monthly_charge"].fillna(0)
    merged["data_usage_gb"] = merged["data_usage_gb"].fillna(0)

    segment_data = merged[[
        "age",
        "monthly_charge",
        "data_usage_gb"
    ]]

    kmeans = KMeans(n_clusters=4, random_state=42)
    merged["segment"] = kmeans.fit_predict(segment_data)

    segment_labels = {
        0: "VIP Customers",
        1: "Heavy Users",
        2: "Budget Users",
        3: "At Risk Group"
    }

    merged["segment_name"] = merged["segment"].map(segment_labels)

    seg_fig = px.scatter(
        merged,
        x="monthly_charge",
        y="data_usage_gb",
        color="segment_name",
        hover_data=["customer_id"],
        title="Customer Segmentation Map"
    )

    st.plotly_chart(seg_fig, use_container_width=True)

    st.dataframe(
        merged[[
            "customer_id",
            "age",
            "monthly_charge",
            "data_usage_gb",
            "segment_name"
        ]],
        use_container_width=True
    )

# ---------------- ANOMALY DETECTION ----------------
elif selected == "Anomaly Detection":

    st.title("🚨 Anomaly Detection Center")

    anomaly_df = customers.merge(
        billing.groupby("customer_id")["payment_delay_days"].mean().reset_index(),
        on="customer_id",
        how="left"
    )

    anomaly_df = anomaly_df.merge(
        tickets.groupby("customer_id").size().reset_index(name="ticket_count"),
        on="customer_id",
        how="left"
    )

    anomaly_df["payment_delay_days"] = anomaly_df["payment_delay_days"].fillna(0)
    anomaly_df["ticket_count"] = anomaly_df["ticket_count"].fillna(0)

    features = anomaly_df[[
        "age",
        "payment_delay_days",
        "ticket_count"
    ]]

    detector = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    anomaly_df["anomaly"] = detector.fit_predict(features)

    suspicious = anomaly_df[anomaly_df["anomaly"] == -1]

    st.metric("Suspicious Customers", len(suspicious))

    anomaly_fig = px.scatter(
        suspicious,
        x="payment_delay_days",
        y="ticket_count",
        color="churn",
        hover_data=["customer_id"],
        title="Suspicious Customer Behavior"
    )

    st.plotly_chart(anomaly_fig, use_container_width=True)

    st.dataframe(
        suspicious[[
            "customer_id",
            "age",
            "payment_delay_days",
            "ticket_count",
            "churn"
        ]],
        use_container_width=True
    )

# ---------------- HIGH RISK WATCHLIST ----------------
elif selected == "High Risk Watchlist":

    st.title("🛡 High Risk Monitoring Center")

    risk_df = customers.merge(
        billing.groupby("customer_id")["payment_delay_days"].mean().reset_index(),
        on="customer_id",
        how="left"
    )

    risk_df = risk_df.merge(
        tickets.groupby("customer_id").size().reset_index(name="ticket_count"),
        on="customer_id",
        how="left"
    )

    risk_df["payment_delay_days"] = risk_df["payment_delay_days"].fillna(0)
    risk_df["ticket_count"] = risk_df["ticket_count"].fillna(0)

    high_risk = risk_df[
        (risk_df["payment_delay_days"] > 10) |
        (risk_df["ticket_count"] > 5)
    ]

    st.metric("High Risk Customers", len(high_risk))

    st.dataframe(high_risk, use_container_width=True)

    csv = high_risk.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download High Risk Report",
        csv,
        "high_risk_customers.csv",
        "text/csv"
    )



