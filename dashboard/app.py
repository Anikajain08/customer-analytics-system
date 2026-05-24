import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

from src.segmentation import segment_customers
from src.churn_prediction import predict_churn
from auth.login import login
from src.database import add_user

# session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# ✅ THIS MUST BE OUTSIDE
if not st.session_state.logged_in:
    st.title("🔐 Authentication")

    option = st.radio("Select Option", ["Login", "Sign Up"])

    # 🔑 LOGIN
    if option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            role = login(username, password)

            if role:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success(f"Welcome {username} ({role})")
                st.rerun()
            else:
                st.error("Invalid credentials")
                
        elif option == "Sign Up":
            st.warning("Signup disabled in cloud version. Use demo credentials below.")
    
    st.stop()


st.title("Customer Analytics Dashboard")

# upload first
uploaded_file = st.file_uploader("Upload Dataset")

if uploaded_file:

    # read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
    else:
        @st.cache_data
        def load_data(file):
            return pd.read_excel(file)
        df = load_data(uploaded_file)
      
    st.write("Sample Customer IDs:", list(df['CustomerID'].dropna().astype(int).unique())[:10])
        
    # show raw data
    st.write("Raw Data", df.head())

    # KPIs
    st.subheader("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", int(df['Quantity'].mul(df['UnitPrice']).sum()))
    col2.metric("Total Customers", df['CustomerID'].nunique())
    col3.metric("Total Orders", df['InvoiceNo'].nunique())

    # segmentation + churn
    rfm = segment_customers(df)
    rfm = predict_churn(rfm)

    st.subheader("📋 Customer Segments")
    st.write(rfm.head())    
    
    from src.recommendation import recommend_products
    st.subheader("🎁 Product Recommendation")
    customer_id = st.number_input("Enter Customer ID", step=1)
    
    if st.button("Get Recommendations"):
        recs = recommend_products(df, customer_id)
        if isinstance(recs, str):
            st.error(recs)
        else:
            st.write(recs)
    if customer_id:
        recs = recommend_products(df, customer_id)

    if st.button("Get Recommendations"):
        recs = recommend_products(df, customer_id)
        st.write(recs)
    
    if isinstance(recs, str):
        st.error(recs)
    else:
        st.write(recs) 
    
    from src.demand_prediction import predict_demand
    st.subheader("📦 Inventory Demand Prediction")
    day = st.number_input("Day", min_value=1, max_value=31, step=1)
    month = st.number_input("Month", min_value=1, max_value=12, step=1)
    year = st.number_input("Year", min_value=2010, max_value=2025, step=1)
    
    if st.button("Predict Demand"):
        demand = predict_demand(day, month, year)
        st.success(f"Predicted Demand: {int(demand)} units")
    
    from src.forecasting import predict_sales
    st.subheader("🔮 Sales Forecasting")
    f_day = st.number_input("Forecast Day", min_value=1, max_value=31, step=1)
    f_month = st.number_input("Forecast Month", min_value=1, max_value=12, step=1)
    f_year = st.number_input("Forecast Year", min_value=2010, max_value=2030, step=1)
    
    if st.button("Predict Sales"):
        prediction = predict_sales(f_day, f_month, f_year)
        st.success(f"Predicted Sales: ₹ {int(prediction)}")
        
