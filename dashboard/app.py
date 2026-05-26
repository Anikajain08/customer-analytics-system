
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.segmentation import segment_customers
from src.churn_prediction import predict_churn
from src.recommendation import recommend_products
from src.forecasting import predict_sales
from auth.login import login

st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

/* Sidebar title */
.sidebar-title {
    font-size: 22px;
    font-weight: bold;
    color: #60a5fa;
    margin-bottom: 20px;
}

/* Radio buttons styling */
div[role="radiogroup"] label {
    background: #1f2937;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 8px;
    display: block;
    transition: 0.3s;
}

/* Hover effect */
div[role="radiogroup"] label:hover {
    background: #374151;
    cursor: pointer;
}

/* Selected option */
div[role="radiogroup"] input:checked + div {
    background: #2563eb !important;
    color: white !important;
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)

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
    
st.sidebar.markdown('<div class="sidebar-title">📊 Analytics Panel</div>', unsafe_allow_html=True)
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "👥 Segmentation", "🔄 Churn", "🎯 Recommendation", "📈 Forecasting", "📦 Inventory"]
)


st.title("Customer Analytics Dashboard")

# upload first
uploaded_file = st.file_uploader("Upload Dataset")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file) 

    # create TotalPrice
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    st.success("✅ Data uploaded successfully")
    
    if page == "🏠 Dashboard":
        st.title("📊 Customer Sales Dashboard")
    
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Total Sales", f"₹{df['TotalPrice'].sum():,.0f}")
        col2.metric("📦 Orders", df['InvoiceNo'].nunique())
        col3.metric("👤 Customers", df['CustomerID'].nunique())
        col4.metric("📈 Avg Value", f"₹{df['TotalPrice'].mean():.2f}")
        
        st.markdown("---")
        
        
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    
        monthly = df.groupby('Month')['TotalPrice'].sum().reset_index()
        country = df.groupby('Country')['TotalPrice'].sum().reset_index()
    
        # 📈 Charts
        fig1 = px.line(monthly, x='Month', y='TotalPrice', title="Monthly Sales")
        fig2 = px.bar(country.head(10), x='Country', y='TotalPrice', title="Sales by Country")
    
        fig1.update_layout(template="plotly_dark")
        fig2.update_layout(template="plotly_dark")
    
        # 🔥 Layout (Main + Side Panel)
        col1, col2 = st.columns([3,1])
    
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)
    
        with col2:
            st.markdown("### 👤 Profile")
            st.markdown("""
                    <div style="background:#1c1f26;padding:15px;border-radius:10px;">
                    <h4>User: Admin</h4>
                    <p>Role: Analyst</p>
                    <p>Status: Active</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif page == "👥 Segmentation":
        rfm = segment_customers(df)
        
        if 'Segment' in rfm.columns:
            segment = rfm['Segment'].value_counts().reset_index()
            segment.columns = ['Segment', 'Count']
            fig3 = px.pie(segment, names='Segment', values='Count',
                  title="Customer Segmentation")
            
            fig3.update_layout(template="plotly_dark")
        
            st.plotly_chart(fig3, use_container_width=True)
    
        else:
            st.warning("⚠️ Segment column not found")
    
    elif page == "🔄 Churn":
        st.title("🔄 Churn Prediction")
        rfm = segment_customers(df)
        churn_df = predict_churn(rfm)

        st.write(churn_df.head())
    
    elif page == "🎯 Recommendation":
        st.title("🎯 Product Recommendation")
        customer_id = st.number_input("Enter Customer ID", step=1)
        
        if st.button("Recommend"):
            st.write("Function loaded ✅")
            recs = recommend_products(df, customer_id)
            if recs:
                st.write("Recommended Products:")
                st.write(recs)
            else:
                st.warning("⚠️ No recommendations found")
    
    elif page == "📈 Forecasting":
        st.title("📈 Sales Forecasting")
        
        forecast = predict_sales(df)
        
        if forecast is not None:
            st.write(forecast)
        else:
            st.warning("⚠️ No forecast data available")
    
    elif page == "📦 Inventory":
        st.title("📦 Inventory Demand")
        
        demand = predict_demand(df)
        st.write(demand)
        
    else:
        st.info("ℹ️ Please upload dataset or check required columns")