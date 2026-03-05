import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("fraud_model.pkl")

st.title("AI Fraud Detection System")

st.write("Enter order details to calculate fraud risk.")

# User Inputs
amount = st.number_input("Transaction Amount", min_value=0.0, value=100.0)

num_orders_last_7_days = st.number_input(
    "Number of Orders in Last 7 Days",
    min_value=0,
    value=1
)

is_first_time_buyer = st.selectbox(
    "Is First Time Buyer?",
    [0,1]
)

country_mismatch = st.selectbox(
    "Billing and Shipping Country Mismatch?",
    [0,1]
)

payment_avs_result = st.selectbox(
    "AVS Result (Address Match)",
    [1,0]  # 1=match, 0=fail
)

payment_cvv_result = st.selectbox(
    "CVV Result",
    [1,0]  # 1=match, 0=fail
)

# Create input dataframe
input_data = pd.DataFrame({
    "amount":[amount],
    "is_first_time_buyer":[is_first_time_buyer],
    "payment_avs_result":[payment_avs_result],
    "payment_cvv_result":[payment_cvv_result],
    "num_orders_last_7_days":[num_orders_last_7_days],
    "country_mismatch":[country_mismatch]
})

# Prediction
if st.button("Check Fraud Risk"):

    fraud_prob = model.predict_proba(input_data)[0][1]

    st.subheader("Fraud Probability")
    st.write(round(fraud_prob,3))

    # Action recommendation
    if fraud_prob > 0.8:
        action = "Cancel Order"
    elif fraud_prob > 0.5:
        action = "Manual Verification"
    else:
        action = "Approve"

    st.subheader("Recommended Action")
    st.write(action)